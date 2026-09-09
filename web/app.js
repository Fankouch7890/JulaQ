document.addEventListener("DOMContentLoaded", () => {
    const robotsContainer = document.getElementById("robots-container");
    const factoryFloor = document.getElementById("factory-floor");
    const robotSelect = document.getElementById("robot-select");
    const refreshBtn = document.getElementById("refresh-robots-btn");
    const controlFeedback = document.getElementById("control-feedback");
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatMessages = document.getElementById("chat-messages");

    // Command buttons
    const cmdMove = document.getElementById("cmd-move");
    const cmdStop = document.getElementById("cmd-stop");
    const cmdStatus = document.getElementById("cmd-status");
    const cmdEmergency = document.getElementById("cmd-emergency");

    let robotsData = [];

    // Map positions to canvas % coordinates
    const floorPositions = {
        "Zone A": { top: "20%", right: "20%" },
        "Zone B": { top: "20%", right: "70%" },
        "Zone C": { top: "65%", right: "30%" },
        "Zone D": { top: "65%", right: "75%" },
        "Dock 1": { top: "10%", right: "10%" },
        "Station 1": { top: "80%", right: "80%" }
    };

    // Fetch and render robots
    async function loadRobots() {
        try {
            const res = await fetch("/api/robots");
            const data = await res.json();
            robotsData = data.robots || [];
            renderRobotsList();
            renderFactoryFloor();
        } catch (err) {
            console.error("Error fetching robots:", err);
            robotsContainer.innerHTML = `<div class="control-feedback">⚠️ تعذر اتصال الخادم بالروبوتات</div>`;
        }
    }

    function renderRobotsList() {
        if (!robotsData.length) {
            robotsContainer.innerHTML = `<div>لا توجد بيانات للروبوتات</div>`;
            return;
        }

        robotsContainer.innerHTML = robotsData.map(r => {
            const isMoving = r.status === 'moving' || r.status === 'تحرك';
            const statusClass = isMoving ? 'moving' : (r.status === 'stopped' ? 'stopped' : 'idle');
            const posStr = typeof r.position === 'object' ? `X: ${r.position[0]}, Y: ${r.position[1]}` : r.position;

            return `
                <div class="robot-card-item">
                    <div class="robot-header">
                        <span class="robot-name">🤖 ${r.robot_id}</span>
                        <span class="status-badge ${statusClass}">${r.status}</span>
                    </div>
                    <div class="robot-info">
                        <span>📍 الموقع: ${posStr}</span>
                        <span>🔋 البطارية: ${r.battery}%</span>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${r.battery}%; background-color: ${r.battery < 20 ? '#ef4444' : '#22c55e'};"></div>
                        </div>
                    </div>
                </div>
            `;
        }).join("");
    }

    function renderFactoryFloor() {
        factoryFloor.innerHTML = "";
        robotsData.forEach((r, idx) => {
            const marker = document.createElement("div");
            const isMoving = r.status === 'moving' || r.status === 'تحرك';
            marker.className = `robot-marker ${isMoving ? 'moving' : ''}`;

            // Calculate pseudo position on visual floor
            const posKeys = Object.keys(floorPositions);
            const posKey = posKeys[idx % posKeys.length];
            const coords = floorPositions[posKey] || { top: `${30 + idx * 15}%`, right: `${20 + idx * 20}%` };

            marker.style.top = coords.top;
            marker.style.right = coords.right;
            marker.innerHTML = `R${idx + 1}`;
            marker.title = `${r.robot_id} - ${r.status}`;

            marker.addEventListener("click", () => {
                robotSelect.value = r.robot_id;
                showFeedback(`تم اختيار الروبوت: ${r.robot_id}`);
            });

            factoryFloor.appendChild(marker);
        });
    }

    function showFeedback(msg, isError = false) {
        controlFeedback.classList.remove("hidden");
        controlFeedback.style.borderColor = isError ? "var(--accent-danger)" : "var(--accent-blue)";
        controlFeedback.innerText = msg;
        setTimeout(() => {
            controlFeedback.classList.add("hidden");
        }, 4000);
    }

    // Direct Robot Controls
    async function executeRobotCommand(endpoint, robotId) {
        try {
            showFeedback(`جاري إرسال الأمر إلى ${robotId}...`);
            const res = await fetch(`/api/robot/${endpoint}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ robot_id: robotId })
            });
            const data = await res.json();
            showFeedback(`النتيجة (${robotId}): ${data.status || 'نجاح الإجراء'}`);
            await loadRobots();
        } catch (err) {
            showFeedback(`حدث خطأ أثناء التنفيذ: ${err}`, true);
        }
    }

    cmdMove.addEventListener("click", () => executeRobotCommand("move", robotSelect.value));
    cmdStop.addEventListener("click", () => executeRobotCommand("stop", robotSelect.value));
    cmdStatus.addEventListener("click", () => executeRobotCommand("status", robotSelect.value));
    cmdEmergency.addEventListener("click", () => executeRobotCommand("stop", robotSelect.value));

    refreshBtn.addEventListener("click", loadRobots);

    // AI Chat Handler
    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (!text) return;

        appendMessage(text, "user");
        chatInput.value = "";

        const loadingMsg = appendMessage("جاري التفكير والمعالجة...", "ai");

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();

            // Remove loading msg
            loadingMsg.remove();

            appendMessage(data.reply, "ai");
            await loadRobots();
        } catch (err) {
            loadingMsg.remove();
            appendMessage(`⚠️ تعذر الاتصال بالوكيل الذكي: ${err}`, "ai");
        }
    });

    // Quick prompt chips
    document.querySelectorAll(".prompt-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            chatInput.value = chip.dataset.cmd;
            chatForm.dispatchEvent(new Event("submit"));
        });
    });

    function appendMessage(text, sender) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${sender}-message`;
        msgDiv.innerHTML = `<div class="msg-bubble">${escapeHtml(text)}</div>`;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return msgDiv;
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    // Initial load
    loadRobots();
    setInterval(loadRobots, 10000); // auto-refresh every 10s
});
