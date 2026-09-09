// Pi ImmoChain Tunisia - JavaScript Application Logic

// Initial Real Estate Data in Tunisia
const initialProperties = [
    {
        id: 1,
        title: "فيلّة فخمة متطلة على البحر بحمامات Yasmine",
        governorate: "Hammamet",
        type: "villa",
        deal: "sale",
        pricePi: 4500,
        priceTnd: "1,450,000 د.ت",
        bedrooms: 4,
        bathrooms: 3,
        area: 380,
        image: "https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=800&q=80",
        description: "فيلّة حديثة فاخرة مع مسبح خاص وحديقة شاسعة تقع في منطقة ياسمين الحمامات المتميزة.",
        owner: "املاك حمامات العقارية"
    },
    {
        id: 2,
        title: "شقة S+2 راقية في ضفاف البحيرة 2",
        governorate: "Tunis",
        type: "apartment",
        deal: "rent",
        pricePi: 45,
        priceTnd: "2,200 د.ت / شهرياً",
        bedrooms: 2,
        bathrooms: 2,
        area: 120,
        image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80",
        description: "شقة مفروشة بأرقى الأثاث في أرقى مناطق ضفاف البحيرة 2 Tunis، حراسة 24/24 وموقف سيارات مغطى.",
        owner: "محمد علي التونسي"
    },
    {
        id: 3,
        title: "أرض معدّة للبناء بالقرب من الشاطئ بسوسة القنطاوي",
        governorate: "Sousse",
        type: "land",
        deal: "sale",
        pricePi: 1800,
        priceTnd: "580,000 د.ت",
        bedrooms: 0,
        bathrooms: 0,
        area: 600,
        image: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
        description: "قطعة أرض شهادة ملكية فردية ممتازة للبناء الاستثماري أو فيلة سكنية بالقرب من المرفأ الترفيهي للقنطاوي.",
        owner: "شركة الساحل للاستثمار"
    },
    {
        id: 4,
        title: "شقة S+3 مطلة على بحر القنطاوي سوسة",
        governorate: "Sousse",
        type: "apartment",
        deal: "sale",
        pricePi: 1250,
        priceTnd: "390,000 د.ت",
        bedrooms: 3,
        bathrooms: 2,
        area: 150,
        image: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80",
        description: "شقة مطلة مباشرة على البحر في الإقامة السكنية القنطاوي سوسة مع مصعد وحراسة.",
        owner: "عقارات سوسة"
    },
    {
        id: 5,
        title: "فيلّة تقليدية فاخرة مع مسبح في جربة حومة السوق",
        governorate: "Djerba",
        type: "villa",
        deal: "sale",
        pricePi: 3200,
        priceTnd: "980,000 د.ت",
        bedrooms: 3,
        bathrooms: 3,
        area: 450,
        image: "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
        description: "حوش جربي فاخر مرمم بأحدث المعايير مع مسبح وسط الطبيعة الهادئة بجربة.",
        owner: "جربة إموبيليي"
    },
    {
        id: 6,
        title: "محل تجاري في موقع استراتيجي بصفاقس المدينة",
        governorate: "Sfax",
        type: "commercial",
        deal: "rent",
        pricePi: 60,
        priceTnd: "3,000 د.ت / شهرياً",
        bedrooms: 0,
        bathrooms: 1,
        area: 90,
        image: "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=800&q=80",
        description: "محل تجاري ممتاز ومناسب لجميع النشاطات التجارية في وسط مدينة صفاقس التجاري.",
        owner: "أحمد الصفاقسي"
    }
];

// App State
let properties = [...initialProperties];
let currentUser = null;
let currentSelectedProperty = null;

// Initialize Pi Network SDK
document.addEventListener('DOMContentLoaded', () => {
    initPiSDK();
    renderProperties(properties);
    setupEventListeners();
});

function initPiSDK() {
    try {
        if (typeof Pi !== 'undefined') {
            Pi.init({ version: "2.0", sandbox: true });
            console.log("Pi Network SDK initialized successfully");
        } else {
            console.warn("Pi SDK not loaded. Running in web preview mode.");
        }
    } catch (err) {
        console.error("Error initializing Pi SDK:", err);
    }
}

// User Authentication with Pi
async function authenticatePiUser() {
    if (typeof Pi === 'undefined') {
        alert("أنت حالياً تستخدم متصفح عادي. يرجى فتح التطبيق من متصفح Pi Browser للربط الكامل مع المحفظة.");
        currentUser = { username: "مستخدم تجريبي (Pi Browser)", uid: "demo123" };
        updateUIWithUser();
        return;
    }

    const scopes = ['username', 'payments'];

    try {
        const auth = await Pi.authenticate(scopes, onIncompletePaymentFound);
        currentUser = auth.user;
        updateUIWithUser();
        alert(`أهلاً بك يا ${currentUser.username}! تم الاتصال بحساب Pi بنجاح.`);
    } catch (error) {
        console.error("Pi Auth failed:", error);
        alert("فشل الاتصال بحساب Pi Network. يرجى المحاولة لاحقاً.");
    }
}

function updateUIWithUser() {
    const authBtnContainer = document.getElementById('authContainer');
    if (currentUser) {
        authBtnContainer.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px; background: #f3e8ff; padding: 6px 14px; border-radius: 20px; color: #6d28d9; font-weight: bold;">
                <i class="fas fa-user-circle"></i>
                <span>${currentUser.username}</span>
            </div>
        `;
    }
}

function onIncompletePaymentFound(payment) {
    console.log("Incomplete payment found:", payment);
    // Submit incomplete payment for resolution if needed
}

// Render Properties
function renderProperties(items) {
    const grid = document.getElementById('propertiesGrid');
    if (items.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #64748b;"> لا توجد عقارات مطابقة للبحث حالياً. </div>`;
        return;
    }

    grid.innerHTML = items.map(p => `
        <div class="property-card">
            <div class="property-image">
                <img src="${p.image}" alt="${p.title}" />
                <div class="property-badges">
                    <span class="badge ${p.deal === 'sale' ? 'badge-sale' : 'badge-rent'}">
                        ${p.deal === 'sale' ? 'للبيع' : 'للكراء'}
                    </span>
                    <span class="badge badge-pi">
                        <i class="fab fa-product-hunt"></i> Pi Immo
                    </span>
                </div>
                <div class="property-price">
                    <i class="fab fa-product-hunt"></i> ${p.pricePi.toLocaleString()} Pi
                </div>
            </div>
            <div class="property-body">
                <h3 class="property-title">${p.title}</h3>
                <div class="property-location">
                    <i class="fas fa-map-marker-alt" style="color: #ef4444;"></i> ${getGovName(p.governorate)} - تونس
                </div>
                <div class="property-features">
                    ${p.bedrooms ? `<span><i class="fas fa-bed"></i> ${p.bedrooms} غرف</span>` : ''}
                    ${p.bathrooms ? `<span><i class="fas fa-bath"></i> ${p.bathrooms} حمام</span>` : ''}
                    <span><i class="fas fa-ruler-combined"></i> ${p.area} م²</span>
                </div>
                <div class="property-footer">
                    <button class="btn btn-pi btn-block" onclick="openPropertyDetails(${p.id})">
                        <i class="fas fa-eye"></i> عرض التفاصيل وحجز بالـ Pi
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

function getGovName(code) {
    const names = {
        'Tunis': 'تونس العاصمة',
        'Sousse': 'سوسة',
        'Hammamet': 'حمامات (نابل)',
        'Sfax': 'صفاقس',
        'Monastir': 'المنستير',
        'Djerba': 'جربة (مدنين)',
        'Bizerte': 'بنزرت'
    };
    return names[code] || code;
}

// Filter Functionality
function filterProperties() {
    const gov = document.getElementById('filterGov').value;
    const deal = document.getElementById('filterDeal').value;
    const type = document.getElementById('filterType').value;

    const filtered = properties.filter(p => {
        const matchesGov = gov === 'all' || p.governorate === gov;
        const matchesDeal = deal === 'all' || p.deal === deal;
        const matchesType = type === 'all' || p.type === type;
        return matchesGov && matchesDeal && matchesType;
    });

    renderProperties(filtered);
}

// Modal View Details
function openPropertyDetails(id) {
    const p = properties.find(item => item.id === id);
    if (!p) return;

    currentSelectedProperty = p;
    const content = document.getElementById('detailModalContent');

    content.innerHTML = `
        <img src="${p.image}" alt="${p.title}" style="width: 100%; height: 260px; object-fit: cover; border-radius: 8px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span class="badge ${p.deal === 'sale' ? 'badge-sale' : 'badge-rent'}">${p.deal === 'sale' ? 'للبيع' : 'للكراء'}</span>
            <div style="font-size: 1.4rem; font-weight: 800; color: #8b5cf6;">
                <i class="fab fa-product-hunt"></i> ${p.pricePi.toLocaleString()} Pi
                <span style="font-size: 0.9rem; color: #64748b; font-weight: normal;">(${p.priceTnd})</span>
            </div>
        </div>
        <h2 style="font-size: 1.4rem; margin-bottom: 8px;">${p.title}</h2>
        <p style="color: #64748b; margin-bottom: 16px;"><i class="fas fa-map-marker-alt"></i> ${getGovName(p.governorate)} - تونس</p>

        <p style="margin-bottom: 20px; line-height: 1.7; background: #f8fafc; padding: 12px; border-radius: 8px;">${p.description}</p>

        <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="color: #1e40af; margin-bottom: 6px;"><i class="fas fa-shield-alt"></i> ضمان المعاملة عبر Pi Network Smart Contract</h4>
            <p style="font-size: 0.85rem; color: #1e3a8a;">عند دفع العربون أو الشراء بواسطة عملة Pi، يتم توثيق العملية وتقييد العقار باسمك مع صاحب العقار مباشرة.</p>
        </div>

        <div style="display: flex; gap: 12px;">
            <button class="btn btn-pi btn-block" onclick="buyWithPi(${p.id})">
                <i class="fab fa-product-hunt"></i> دفع عربون / شحن العقد (10 Pi)
            </button>
            <button class="btn btn-primary btn-block" onclick="contactOwner('${p.owner}')">
                <i class="fas fa-phone-alt"></i> الاتصال بالمالك
            </button>
        </div>
    `;

    document.getElementById('propertyModal').classList.add('active');
}

function closeDetailModal() {
    document.getElementById('propertyModal').classList.remove('active');
}

function openAddModal() {
    document.getElementById('addModal').classList.add('active');
}

function closeAddModal() {
    document.getElementById('addModal').classList.remove('active');
}

function contactOwner(owner) {
    alert(`صاحب العقار: ${owner}\nرقم التواصل التونسي: +216 71 000 000 / +216 98 000 000`);
}

// Add New Property
function handleAddProperty(e) {
    e.preventDefault();

    const newProp = {
        id: properties.length + 1,
        title: document.getElementById('newTitle').value,
        governorate: document.getElementById('newGov').value,
        type: document.getElementById('newType').value,
        deal: document.getElementById('newDeal').value,
        pricePi: parseFloat(document.getElementById('newPricePi').value),
        priceTnd: `${document.getElementById('newPriceTnd').value} د.ت`,
        image: document.getElementById('newImage').value || 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=800&q=80',
        description: document.getElementById('newDesc').value,
        owner: currentUser ? currentUser.username : "مستخدم Pi"
    };

    properties.unshift(newProp);
    renderProperties(properties);
    closeAddModal();
    alert("تم إضافة عقارك بنجاح في منصة Pi ImmoChain Tunisia!");
}

// Handle Payment via Pi SDK
async function buyWithPi(propertyId) {
    if (!currentUser) {
        alert("يرجى تسجيل الدخول بحساب Pi أولاً لتأفيذ المعاملة المالية.");
        await authenticatePiUser();
        if (!currentUser) return;
    }

    const amount = 10; // Demo Deposit amount in Pi

    if (typeof Pi === 'undefined') {
        alert(`تم المحاكاة بنجاح! تم دفع ${amount} Pi لحجز العقار رقم #${propertyId} في تونس.`);
        closeDetailModal();
        return;
    }

    try {
        const paymentData = {
            amount: amount,
            memo: `عربون حجز عقار #${propertyId} - Pi ImmoChain Tunisia`,
            metadata: { propertyId: propertyId }
        };

        const callbacks = {
            onReadyForServerApproval: function(paymentId) {
                console.log("Ready for server approval:", paymentId);
                // In production, notify backend server to approve payment
            },
            onReadyForServerCompletion: function(paymentId, txid) {
                console.log("Ready for server completion:", paymentId, txid);
                alert(`مبروك! تم إتمام عملية دفع ${amount} Pi لحجز العقار بنجاح برقم المعاملة:\n${txid}`);
                closeDetailModal();
            },
            onCancel: function(paymentId) {
                console.log("Payment canceled:", paymentId);
                alert("تم إلغاء عملية الدفع.");
            },
            onError: function(error, payment) {
                console.error("Payment error:", error, payment);
                alert("حدث خطأ أثناء إجراء الدفع عبر شبكة Pi.");
            }
        };

        await Pi.createPayment(paymentData, callbacks);
    } catch (err) {
        console.error("Error creating payment:", err);
        alert("تعذر فتح واجهة الدفع في Pi Browser.");
    }
}

// Setup listeners
function setupEventListeners() {
    document.getElementById('filterGov').addEventListener('change', filterProperties);
    document.getElementById('filterDeal').addEventListener('change', filterProperties);
    document.getElementById('filterType').addEventListener('change', filterProperties);
    document.getElementById('addPropertyForm').addEventListener('submit', handleAddProperty);
}
