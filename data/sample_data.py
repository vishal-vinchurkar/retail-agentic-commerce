import random
import hashlib

DIVISIONS = {
    "HOME_LIVING": {
        "id": "DIV-001",
        "name": "Home & Living",
        "margin_target": 0.42,
        "categories": ["Furniture", "Homewares", "Bedding", "Kitchen", "Storage", "Bathroom", "Decor"],
        "annual_revenue": 2.8e9,
        "sku_count": 45000,
        "suppliers": 340,
        "distribution_centers": ["SYD-DC-01", "MEL-DC-02", "BNE-DC-03"]
    },
    "APPAREL": {
        "id": "DIV-002", 
        "name": "Apparel & Accessories",
        "margin_target": 0.55,
        "categories": ["Women", "Men", "Kids", "Baby", "Footwear", "Accessories", "Activewear"],
        "annual_revenue": 3.2e9,
        "sku_count": 85000,
        "suppliers": 520,
        "distribution_centers": ["SYD-DC-01", "MEL-DC-02", "PER-DC-04"]
    },
    "ELECTRONICS": {
        "id": "DIV-003",
        "name": "Electronics & Entertainment", 
        "margin_target": 0.28,
        "categories": ["Audio", "Gaming", "Smart Home", "Phones", "Cameras", "Wearables", "Media"],
        "annual_revenue": 1.9e9,
        "sku_count": 22000,
        "suppliers": 180,
        "distribution_centers": ["SYD-DC-01", "MEL-DC-02"]
    },
    "OUTDOOR_HARDWARE": {
        "id": "DIV-004",
        "name": "Outdoor & Hardware",
        "margin_target": 0.38,
        "categories": ["Garden", "Tools", "Outdoor Living", "Automotive", "Paint", "Camping", "Sports"],
        "annual_revenue": 4.1e9,
        "sku_count": 120000,
        "suppliers": 890,
        "distribution_centers": ["SYD-DC-01", "MEL-DC-02", "BNE-DC-03", "PER-DC-04", "ADL-DC-05"]
    },
    "OFFICE_TECH": {
        "id": "DIV-005",
        "name": "Office & Technology",
        "margin_target": 0.32,
        "categories": ["Computers", "Printers", "Office Supplies", "Furniture", "Tech Accessories", "Monitors"],
        "annual_revenue": 2.4e9,
        "sku_count": 35000,
        "suppliers": 420,
        "distribution_centers": ["SYD-DC-01", "MEL-DC-02", "BNE-DC-03"]
    },
    "TOYS_ENTERTAINMENT": {
        "id": "DIV-006",
        "name": "Toys & Entertainment",
        "margin_target": 0.45,
        "categories": ["Toys", "Games", "Books", "Movies", "Party", "Arts & Crafts"],
        "annual_revenue": 1.5e9,
        "sku_count": 28000,
        "suppliers": 280,
        "distribution_centers": ["SYD-DC-01", "MEL-DC-02", "BNE-DC-03"]
    },
    "HEALTH_BEAUTY": {
        "id": "DIV-007",
        "name": "Health & Beauty",
        "margin_target": 0.48,
        "categories": ["Personal Care", "Cosmetics", "Health", "Fitness", "Haircare", "Skincare"],
        "annual_revenue": 1.2e9,
        "sku_count": 18000,
        "suppliers": 220,
        "distribution_centers": ["SYD-DC-01", "MEL-DC-02"]
    }
}

DISTRIBUTION_CENTERS = {
    "SYD-DC-01": {
        "name": "Sydney Distribution Centre",
        "location": {"lat": -33.8688, "lng": 151.2093, "suburb": "Moorebank", "state": "NSW"},
        "capacity_pallets": 85000,
        "automation_level": "HIGH",
        "capabilities": ["cross-dock", "pick-pack", "returns", "cold-chain"],
        "workforce": 1200,
        "daily_throughput": 180000,
        "stores_served": 245,
        "carriers": ["StarTrack", "Toll", "DHL", "Australia Post"],
        "operating_hours": "24/7"
    },
    "MEL-DC-02": {
        "name": "Melbourne Distribution Centre",
        "location": {"lat": -37.8136, "lng": 144.9631, "suburb": "Truganina", "state": "VIC"},
        "capacity_pallets": 72000,
        "automation_level": "HIGH",
        "capabilities": ["cross-dock", "pick-pack", "returns"],
        "workforce": 980,
        "daily_throughput": 145000,
        "stores_served": 198,
        "carriers": ["StarTrack", "Toll", "TNT"],
        "operating_hours": "24/7"
    },
    "BNE-DC-03": {
        "name": "Brisbane Distribution Centre",
        "location": {"lat": -27.4698, "lng": 153.0251, "suburb": "Richlands", "state": "QLD"},
        "capacity_pallets": 45000,
        "automation_level": "MEDIUM",
        "capabilities": ["cross-dock", "pick-pack", "returns"],
        "workforce": 650,
        "daily_throughput": 95000,
        "stores_served": 142,
        "carriers": ["StarTrack", "Toll", "Northline"],
        "operating_hours": "5AM-11PM"
    },
    "PER-DC-04": {
        "name": "Perth Distribution Centre",
        "location": {"lat": -31.9505, "lng": 115.8605, "suburb": "Canning Vale", "state": "WA"},
        "capacity_pallets": 38000,
        "automation_level": "MEDIUM",
        "capabilities": ["cross-dock", "pick-pack"],
        "workforce": 420,
        "daily_throughput": 65000,
        "stores_served": 89,
        "carriers": ["StarTrack", "Centurion", "CTI"],
        "operating_hours": "5AM-11PM"
    },
    "ADL-DC-05": {
        "name": "Adelaide Distribution Centre",
        "location": {"lat": -34.9285, "lng": 138.6007, "suburb": "Edinburgh Parks", "state": "SA"},
        "capacity_pallets": 28000,
        "automation_level": "MEDIUM",
        "capabilities": ["cross-dock", "pick-pack"],
        "workforce": 280,
        "daily_throughput": 42000,
        "stores_served": 67,
        "carriers": ["StarTrack", "Toll", "Scott's"],
        "operating_hours": "6AM-10PM"
    }
}

SUPPLIERS = [
    {"id": "SUP-001", "name": "Global Home Furnishings Ltd", "country": "China", "port": "Shanghai", "lead_time_days": 45, "divisions": ["HOME_LIVING"], "reliability_score": 0.94},
    {"id": "SUP-002", "name": "TechSource Asia Pacific", "country": "Vietnam", "port": "Ho Chi Minh", "lead_time_days": 35, "divisions": ["ELECTRONICS", "OFFICE_TECH"], "reliability_score": 0.91},
    {"id": "SUP-003", "name": "Australian Apparel Manufacturing", "country": "Australia", "port": "Melbourne", "lead_time_days": 14, "divisions": ["APPAREL"], "reliability_score": 0.97},
    {"id": "SUP-004", "name": "Garden World International", "country": "Thailand", "port": "Bangkok", "lead_time_days": 40, "divisions": ["OUTDOOR_HARDWARE"], "reliability_score": 0.89},
    {"id": "SUP-005", "name": "Premium Tools Co", "country": "Taiwan", "port": "Kaohsiung", "lead_time_days": 38, "divisions": ["OUTDOOR_HARDWARE"], "reliability_score": 0.95},
    {"id": "SUP-006", "name": "Bedding & Soft Furnishings Pty Ltd", "country": "Australia", "port": "Sydney", "lead_time_days": 10, "divisions": ["HOME_LIVING"], "reliability_score": 0.98},
    {"id": "SUP-007", "name": "SoundTech Electronics", "country": "China", "port": "Shenzhen", "lead_time_days": 32, "divisions": ["ELECTRONICS"], "reliability_score": 0.92},
    {"id": "SUP-008", "name": "Toy Kingdom International", "country": "China", "port": "Guangzhou", "lead_time_days": 42, "divisions": ["TOYS_ENTERTAINMENT"], "reliability_score": 0.90},
    {"id": "SUP-009", "name": "Beauty Essentials Co", "country": "Korea", "port": "Busan", "lead_time_days": 28, "divisions": ["HEALTH_BEAUTY"], "reliability_score": 0.93},
    {"id": "SUP-010", "name": "Sports & Outdoor Gear", "country": "Vietnam", "port": "Ho Chi Minh", "lead_time_days": 35, "divisions": ["OUTDOOR_HARDWARE"], "reliability_score": 0.91},
]

BRANDS = {
    "ELECTRONICS": ["SoundWave", "TechEdge", "AudioPro", "SonicMax", "BeatBox", "ClearSound", "EliteAudio", "PulseTech", "VibeTone", "AudioX", "SoundCore", "EchoTech", "Harmony", "BassKing"],
    "HOME_LIVING": ["Coastal Living", "Nordic Home", "Urban Nest", "Sanctuary", "Homecraft", "CasaBlanca", "Artisan Home", "Luxe Living", "Modern Abode", "Hearth & Hand"],
    "APPAREL": ["Autumn Collective", "Urban Edge", "ActiveLife", "Coastal Wear", "StyleCraft", "FitForm", "Everyday Essentials", "Luxe Label", "Comfort Zone", "TrendSetter"],
    "OUTDOOR_HARDWARE": ["ProForce", "GreenTech", "TrailMaster", "PowerPro", "GardenLife", "OutdoorX", "CampKing", "SportZone", "ToolCraft", "YardWorks"],
    "OFFICE_TECH": ["TechEdge", "OfficePro", "WorkSmart", "DigitalMax", "PrintMaster", "DeskCraft", "ErgoTech", "ProDesk", "SmartOffice", "DataCore"],
    "TOYS_ENTERTAINMENT": ["FunZone", "PlayTime", "KidsCraft", "GameWorld", "ToyBox", "CreativeKids", "PartyPro", "Imaginarium", "LearnPlay", "JoyWorld"],
    "HEALTH_BEAUTY": ["GlowUp", "PureEssence", "VitalCare", "BeautyBliss", "FreshStart", "WellnessPlus", "RadiantSkin", "HealthFirst", "NaturalGlow", "FitLife"],
}

PRODUCT_CATALOG = {
    "ELECTRONICS": {
        "Audio": {
            "Headphones": [
                ("Wireless Noise-Cancelling Headphones Pro", 349.00, 299.00, ["premium", "gift", "wireless", "noise-cancelling"]),
                ("Wireless Over-Ear Headphones", 199.00, 179.00, ["wireless", "bluetooth", "comfort"]),
                ("Wireless On-Ear Headphones Compact", 149.00, 129.00, ["portable", "wireless", "lightweight"]),
                ("Studio Monitor Headphones", 279.00, 249.00, ["studio", "professional", "wired", "hi-fi"]),
                ("Gaming Headset RGB", 159.00, 139.00, ["gaming", "rgb", "microphone", "surround"]),
                ("Gaming Headset Pro 7.1", 229.00, 199.00, ["gaming", "7.1-surround", "premium", "microphone"]),
                ("Kids Wireless Headphones", 69.00, 59.00, ["kids", "volume-limited", "safe", "colorful"]),
                ("Sports Wireless Headphones", 129.00, 109.00, ["sports", "sweatproof", "secure-fit"]),
                ("Budget Wireless Headphones", 79.00, 69.00, ["budget", "wireless", "everyday"]),
                ("Premium Audiophile Headphones", 499.00, 449.00, ["audiophile", "hi-res", "premium", "wired"]),
                ("Foldable Travel Headphones", 119.00, 99.00, ["travel", "foldable", "portable", "wireless"]),
                ("Open-Back Reference Headphones", 389.00, 349.00, ["open-back", "reference", "studio", "professional"]),
                ("Bass Boost Wireless Headphones", 169.00, 149.00, ["bass", "wireless", "extra-bass"]),
                ("Retro Style Wireless Headphones", 139.00, 119.00, ["retro", "style", "wireless", "fashion"]),
                ("DJ Professional Headphones", 259.00, 229.00, ["dj", "professional", "swivel", "monitoring"]),
            ],
            "Earbuds": [
                ("True Wireless Earbuds Pro", 299.00, 249.00, ["wireless", "anc", "premium", "gift"]),
                ("True Wireless Earbuds", 149.00, 129.00, ["wireless", "compact", "everyday"]),
                ("Sports Wireless Earbuds", 179.00, 159.00, ["sports", "waterproof", "secure-fit"]),
                ("Budget Wireless Earbuds", 59.00, 49.00, ["budget", "wireless", "basic"]),
                ("Active Noise Cancelling Earbuds", 249.00, 219.00, ["anc", "premium", "wireless"]),
                ("Gaming Wireless Earbuds", 129.00, 109.00, ["gaming", "low-latency", "wireless"]),
                ("Kids Wireless Earbuds", 49.00, 39.00, ["kids", "volume-limited", "colorful"]),
                ("Sleep Earbuds", 199.00, 179.00, ["sleep", "comfort", "noise-masking"]),
                ("Audiophile IEM Earbuds", 399.00, 349.00, ["audiophile", "iem", "hi-res", "premium"]),
                ("Workout Earbuds Secure Fit", 139.00, 119.00, ["workout", "secure", "sweatproof"]),
            ],
            "Speakers": [
                ("Portable Bluetooth Speaker", 89.00, 79.00, ["portable", "bluetooth", "outdoor"]),
                ("Smart Speaker with Voice Assistant", 149.00, 129.00, ["smart", "voice-assistant", "wifi"]),
                ("Premium Bookshelf Speakers (Pair)", 499.00, 449.00, ["bookshelf", "hi-fi", "premium"]),
                ("Outdoor Waterproof Speaker", 129.00, 109.00, ["outdoor", "waterproof", "rugged"]),
                ("Soundbar with Subwoofer", 399.00, 349.00, ["soundbar", "subwoofer", "home-theater"]),
                ("Party Speaker with Lights", 249.00, 219.00, ["party", "lights", "loud", "bluetooth"]),
                ("Mini Portable Speaker", 49.00, 39.00, ["mini", "portable", "compact"]),
                ("Multi-Room Smart Speaker", 199.00, 179.00, ["multi-room", "smart", "wifi"]),
                ("Vinyl Record Player with Speakers", 299.00, 269.00, ["vinyl", "retro", "turntable"]),
                ("Desktop Computer Speakers", 79.00, 69.00, ["desktop", "computer", "usb"]),
            ],
        },
        "Gaming": {
            "Consoles": [
                ("Gaming Console Next-Gen", 749.00, 699.00, ["console", "next-gen", "4k"]),
                ("Gaming Console Digital Edition", 599.00, 549.00, ["console", "digital", "4k"]),
                ("Handheld Gaming Console", 449.00, 399.00, ["handheld", "portable", "gaming"]),
                ("Retro Mini Console", 129.00, 99.00, ["retro", "mini", "classic-games"]),
            ],
            "Controllers": [
                ("Wireless Gaming Controller", 89.00, 79.00, ["wireless", "controller", "gaming"]),
                ("Pro Gaming Controller", 149.00, 129.00, ["pro", "controller", "customizable"]),
                ("Racing Wheel Controller", 399.00, 349.00, ["racing", "wheel", "pedals"]),
                ("Flight Stick Controller", 299.00, 269.00, ["flight", "joystick", "simulator"]),
            ],
            "Accessories": [
                ("Gaming Headset Stand RGB", 49.00, 39.00, ["stand", "rgb", "organizer"]),
                ("Controller Charging Dock", 39.00, 29.00, ["charging", "dock", "controller"]),
                ("Gaming Mouse Pad XL", 29.00, 24.00, ["mousepad", "xl", "gaming"]),
                ("VR Headset Standalone", 549.00, 499.00, ["vr", "virtual-reality", "standalone"]),
            ],
        },
        "Smart Home": {
            "Smart Displays": [
                ("Smart Display 10 inch", 249.00, 219.00, ["smart-display", "voice", "video-calls"]),
                ("Smart Display 7 inch", 149.00, 129.00, ["smart-display", "compact", "voice"]),
                ("Smart Photo Frame", 179.00, 159.00, ["photo-frame", "wifi", "digital"]),
            ],
            "Smart Lighting": [
                ("Smart LED Bulb (4 Pack)", 79.00, 69.00, ["smart", "led", "wifi", "color"]),
                ("Smart Light Strip 5m", 69.00, 59.00, ["light-strip", "rgb", "smart"]),
                ("Smart Floor Lamp", 149.00, 129.00, ["floor-lamp", "smart", "dimmable"]),
                ("Smart Outdoor Lights", 129.00, 109.00, ["outdoor", "smart", "weatherproof"]),
            ],
            "Smart Security": [
                ("Smart Doorbell Camera", 199.00, 179.00, ["doorbell", "camera", "wifi", "security"]),
                ("Indoor Security Camera", 79.00, 69.00, ["camera", "indoor", "wifi", "security"]),
                ("Outdoor Security Camera", 149.00, 129.00, ["camera", "outdoor", "weatherproof"]),
                ("Smart Lock Deadbolt", 299.00, 269.00, ["smart-lock", "keyless", "security"]),
            ],
            "Smart Appliances": [
                ("Robot Vacuum Cleaner", 599.00, 499.00, ["robot", "vacuum", "smart", "mapping"]),
                ("Robot Vacuum with Mop", 799.00, 699.00, ["robot", "vacuum", "mop", "premium"]),
                ("Smart Air Purifier", 349.00, 299.00, ["air-purifier", "smart", "hepa"]),
                ("Smart Thermostat", 249.00, 219.00, ["thermostat", "smart", "energy-saving"]),
            ],
        },
        "Phones": {
            "Smartphones": [
                ("Premium Smartphone 256GB", 1299.00, 1199.00, ["smartphone", "premium", "5g"]),
                ("Mid-Range Smartphone 128GB", 699.00, 599.00, ["smartphone", "mid-range", "5g"]),
                ("Budget Smartphone 64GB", 299.00, 249.00, ["smartphone", "budget", "4g"]),
                ("Senior-Friendly Smartphone", 199.00, 179.00, ["smartphone", "senior", "simple"]),
            ],
            "Phone Accessories": [
                ("Wireless Charger Pad", 49.00, 39.00, ["wireless-charger", "qi", "fast-charge"]),
                ("Wireless Charging Stand", 69.00, 59.00, ["wireless-charger", "stand", "fast"]),
                ("Phone Case Premium", 39.00, 29.00, ["case", "protective", "premium"]),
                ("Screen Protector 3-Pack", 24.00, 19.00, ["screen-protector", "tempered-glass"]),
                ("Car Phone Mount Magnetic", 29.00, 24.00, ["car-mount", "magnetic", "phone"]),
                ("Power Bank 20000mAh", 79.00, 69.00, ["power-bank", "portable", "fast-charge"]),
                ("Power Bank 10000mAh", 49.00, 39.00, ["power-bank", "compact", "travel"]),
            ],
        },
        "Cameras": {
            "Digital Cameras": [
                ("Mirrorless Camera Body", 1499.00, 1349.00, ["mirrorless", "4k", "professional"]),
                ("Compact Digital Camera", 449.00, 399.00, ["compact", "travel", "zoom"]),
                ("Action Camera 4K", 349.00, 299.00, ["action", "4k", "waterproof"]),
                ("Instant Print Camera", 149.00, 129.00, ["instant", "print", "fun"]),
            ],
            "Camera Accessories": [
                ("Camera Tripod Professional", 199.00, 179.00, ["tripod", "professional", "stable"]),
                ("Camera Bag Backpack", 129.00, 109.00, ["bag", "backpack", "protective"]),
                ("Memory Card 128GB", 39.00, 29.00, ["memory-card", "sd", "fast"]),
                ("Camera Lens 50mm", 299.00, 269.00, ["lens", "50mm", "portrait"]),
            ],
        },
        "Wearables": {
            "Smartwatches": [
                ("Premium Smartwatch", 599.00, 549.00, ["smartwatch", "premium", "health"]),
                ("Fitness Smartwatch", 299.00, 269.00, ["smartwatch", "fitness", "gps"]),
                ("Budget Smartwatch", 149.00, 129.00, ["smartwatch", "budget", "basic"]),
                ("Kids Smartwatch GPS", 129.00, 109.00, ["kids", "smartwatch", "gps", "safe"]),
            ],
            "Fitness Trackers": [
                ("Fitness Band Pro", 149.00, 129.00, ["fitness", "band", "heart-rate"]),
                ("Fitness Band Basic", 79.00, 69.00, ["fitness", "band", "steps"]),
                ("Sleep Tracker Ring", 299.00, 269.00, ["sleep", "ring", "health"]),
            ],
        },
    },
    "HOME_LIVING": {
        "Furniture": {
            "Living Room": [
                ("Nordic Minimalist 3-Seater Sofa", 899.00, 799.00, ["sofa", "living-room", "premium", "modern"]),
                ("Modern L-Shaped Sectional Sofa", 1499.00, 1299.00, ["sectional", "l-shape", "large", "premium"]),
                ("Compact 2-Seater Loveseat", 599.00, 549.00, ["loveseat", "compact", "small-space"]),
                ("Recliner Armchair Leather", 799.00, 699.00, ["recliner", "leather", "comfort"]),
                ("Accent Chair Velvet", 349.00, 299.00, ["accent", "velvet", "style"]),
                ("TV Unit Entertainment Center", 449.00, 399.00, ["tv-unit", "entertainment", "storage"]),
                ("Coffee Table Oak", 299.00, 269.00, ["coffee-table", "oak", "wood"]),
                ("Side Table Set of 2", 149.00, 129.00, ["side-table", "set", "modern"]),
                ("Bookshelf 5-Tier", 199.00, 179.00, ["bookshelf", "storage", "display"]),
                ("Floor Lamp Modern", 129.00, 109.00, ["floor-lamp", "lighting", "modern"]),
            ],
            "Bedroom": [
                ("Queen Bed Frame Wood", 599.00, 549.00, ["bed-frame", "queen", "wood"]),
                ("King Bed Frame Upholstered", 899.00, 799.00, ["bed-frame", "king", "upholstered"]),
                ("Single Bed Frame Metal", 249.00, 219.00, ["bed-frame", "single", "metal"]),
                ("Bedside Table Pair", 199.00, 179.00, ["bedside", "nightstand", "pair"]),
                ("Chest of Drawers 6 Drawer", 449.00, 399.00, ["drawers", "storage", "bedroom"]),
                ("Wardrobe 3 Door", 799.00, 699.00, ["wardrobe", "storage", "large"]),
                ("Dressing Table with Mirror", 399.00, 349.00, ["dressing-table", "mirror", "vanity"]),
                ("Mattress Queen Memory Foam", 699.00, 599.00, ["mattress", "queen", "memory-foam"]),
                ("Mattress King Pocket Spring", 999.00, 899.00, ["mattress", "king", "pocket-spring"]),
            ],
            "Dining": [
                ("Dining Table 6-Seater Oak", 699.00, 629.00, ["dining-table", "6-seater", "oak"]),
                ("Dining Chairs Set of 4", 399.00, 349.00, ["dining-chairs", "set", "comfortable"]),
                ("Bar Stools Set of 2", 199.00, 179.00, ["bar-stools", "kitchen", "set"]),
                ("Dining Table Extendable", 899.00, 799.00, ["dining-table", "extendable", "versatile"]),
                ("Buffet Sideboard", 549.00, 499.00, ["buffet", "sideboard", "storage"]),
            ],
            "Office": [
                ("Standing Desk Electric", 699.00, 599.00, ["standing-desk", "electric", "ergonomic"]),
                ("Office Desk Large", 399.00, 349.00, ["desk", "office", "large"]),
                ("Ergonomic Office Chair", 449.00, 399.00, ["office-chair", "ergonomic", "lumbar"]),
                ("Filing Cabinet 3 Drawer", 199.00, 179.00, ["filing-cabinet", "storage", "office"]),
                ("Desk Shelf Organizer", 79.00, 69.00, ["shelf", "organizer", "desk"]),
            ],
        },
        "Kitchen": {
            "Cookware": [
                ("Professional Chef Knife Set (8pc)", 189.00, 149.00, ["knives", "chef", "cooking", "gift"]),
                ("Non-Stick Frying Pan Set", 99.00, 89.00, ["frying-pan", "non-stick", "set"]),
                ("Cast Iron Dutch Oven", 149.00, 129.00, ["dutch-oven", "cast-iron", "cooking"]),
                ("Stainless Steel Pot Set", 249.00, 219.00, ["pots", "stainless-steel", "set"]),
                ("Wok Carbon Steel", 79.00, 69.00, ["wok", "carbon-steel", "asian-cooking"]),
                ("Baking Sheet Set", 49.00, 39.00, ["baking", "sheet", "oven"]),
                ("Mixing Bowl Set Stainless", 59.00, 49.00, ["mixing-bowls", "stainless", "set"]),
            ],
            "Small Appliances": [
                ("Air Fryer 5.5L", 149.00, 129.00, ["air-fryer", "healthy", "cooking"]),
                ("Stand Mixer Professional", 449.00, 399.00, ["stand-mixer", "baking", "professional"]),
                ("Coffee Machine Espresso", 349.00, 299.00, ["coffee", "espresso", "barista"]),
                ("Blender High Power", 199.00, 179.00, ["blender", "smoothie", "powerful"]),
                ("Toaster 4-Slice", 79.00, 69.00, ["toaster", "breakfast", "4-slice"]),
                ("Electric Kettle 1.7L", 59.00, 49.00, ["kettle", "electric", "fast-boil"]),
                ("Food Processor", 179.00, 159.00, ["food-processor", "chopping", "versatile"]),
                ("Slow Cooker 6L", 99.00, 89.00, ["slow-cooker", "easy-meals", "large"]),
                ("Rice Cooker 10-Cup", 89.00, 79.00, ["rice-cooker", "asian", "automatic"]),
                ("Sandwich Press", 49.00, 39.00, ["sandwich", "press", "quick-meals"]),
            ],
            "Cutlery": [
                ("Cutlery Set 24pc Stainless", 79.00, 69.00, ["cutlery", "stainless", "set"]),
                ("Steak Knife Set 6pc", 59.00, 49.00, ["steak-knives", "sharp", "set"]),
                ("Knife Block Set 15pc", 199.00, 179.00, ["knife-block", "complete", "premium"]),
            ],
            "Dinnerware": [
                ("Dinnerware Set 16pc Ceramic", 129.00, 109.00, ["dinnerware", "ceramic", "set"]),
                ("Glassware Set 12pc", 59.00, 49.00, ["glasses", "drinking", "set"]),
                ("Mug Set 6pc", 39.00, 29.00, ["mugs", "coffee", "set"]),
                ("Serving Platter Set", 49.00, 39.00, ["serving", "platter", "entertaining"]),
            ],
        },
        "Bedding": {
            "Sheets": [
                ("Egyptian Cotton Sheet Set (Queen)", 179.00, 149.00, ["sheets", "egyptian-cotton", "luxury"]),
                ("Egyptian Cotton Sheet Set (King)", 199.00, 169.00, ["sheets", "egyptian-cotton", "king"]),
                ("Bamboo Sheet Set (Queen)", 149.00, 129.00, ["sheets", "bamboo", "cooling"]),
                ("Microfiber Sheet Set Budget", 59.00, 49.00, ["sheets", "microfiber", "budget"]),
                ("Linen Sheet Set (Queen)", 249.00, 219.00, ["sheets", "linen", "premium"]),
                ("Flannel Sheet Set Winter", 99.00, 89.00, ["sheets", "flannel", "warm"]),
            ],
            "Quilts & Doonas": [
                ("All Seasons Quilt Queen", 199.00, 179.00, ["quilt", "all-seasons", "versatile"]),
                ("Winter Weight Doona King", 249.00, 219.00, ["doona", "winter", "warm"]),
                ("Lightweight Summer Quilt", 129.00, 109.00, ["quilt", "summer", "light"]),
                ("Kids Character Quilt Single", 79.00, 69.00, ["quilt", "kids", "fun"]),
            ],
            "Pillows": [
                ("Memory Foam Pillow", 79.00, 69.00, ["pillow", "memory-foam", "support"]),
                ("Duck Feather Pillow Pair", 99.00, 89.00, ["pillow", "feather", "luxury"]),
                ("Cooling Gel Pillow", 89.00, 79.00, ["pillow", "cooling", "gel"]),
                ("Body Pillow Long", 59.00, 49.00, ["pillow", "body", "pregnancy"]),
            ],
            "Mattress Protectors": [
                ("Waterproof Mattress Protector Queen", 79.00, 69.00, ["mattress-protector", "waterproof"]),
                ("Bamboo Mattress Topper Queen", 199.00, 179.00, ["mattress-topper", "bamboo", "comfort"]),
            ],
        },
        "Bathroom": {
            "Towels": [
                ("Bath Towel Set 6pc Egyptian Cotton", 99.00, 89.00, ["towels", "bath", "cotton", "set"]),
                ("Beach Towel Oversized", 39.00, 29.00, ["towel", "beach", "oversized"]),
                ("Hand Towel Set 4pc", 39.00, 29.00, ["towels", "hand", "set"]),
                ("Bath Mat Non-Slip", 29.00, 24.00, ["bath-mat", "non-slip", "soft"]),
            ],
            "Storage": [
                ("Bathroom Cabinet Wall Mount", 149.00, 129.00, ["cabinet", "bathroom", "storage"]),
                ("Over Toilet Storage Shelf", 99.00, 89.00, ["storage", "toilet", "shelf"]),
                ("Vanity Organizer", 49.00, 39.00, ["organizer", "vanity", "bathroom"]),
            ],
            "Accessories": [
                ("Shower Curtain Set", 39.00, 29.00, ["shower-curtain", "bathroom", "decor"]),
                ("Bathroom Accessories Set 5pc", 59.00, 49.00, ["accessories", "set", "bathroom"]),
                ("Electric Toothbrush Holder", 29.00, 24.00, ["holder", "toothbrush", "bathroom"]),
            ],
        },
        "Decor": {
            "Wall Art": [
                ("Canvas Print Abstract Large", 149.00, 129.00, ["canvas", "art", "abstract", "large"]),
                ("Photo Frame Set 7pc", 49.00, 39.00, ["frames", "photo", "set"]),
                ("Wall Mirror Decorative", 199.00, 179.00, ["mirror", "decorative", "wall"]),
                ("Metal Wall Art", 129.00, 109.00, ["metal", "art", "modern"]),
            ],
            "Lighting": [
                ("Table Lamp Modern", 79.00, 69.00, ["lamp", "table", "modern"]),
                ("Pendant Light Industrial", 149.00, 129.00, ["pendant", "light", "industrial"]),
                ("Fairy Lights 10m", 24.00, 19.00, ["fairy-lights", "decorative", "string"]),
                ("LED Candles Set 3", 29.00, 24.00, ["candles", "led", "flameless"]),
            ],
            "Soft Furnishings": [
                ("Cushion Cover Set 4pc", 49.00, 39.00, ["cushion", "covers", "set"]),
                ("Throw Blanket Knitted", 79.00, 69.00, ["throw", "blanket", "cozy"]),
                ("Area Rug 160x230cm", 249.00, 219.00, ["rug", "area", "floor"]),
                ("Curtains Blockout Pair", 99.00, 89.00, ["curtains", "blockout", "pair"]),
            ],
        },
        "Storage": {
            "Closet Organization": [
                ("Wardrobe Storage System", 199.00, 179.00, ["wardrobe", "storage", "organization"]),
                ("Hanging Closet Organizer", 39.00, 29.00, ["hanging", "closet", "organizer"]),
                ("Shoe Rack 4-Tier", 49.00, 39.00, ["shoe-rack", "storage", "entryway"]),
                ("Vacuum Storage Bags 10pk", 29.00, 24.00, ["vacuum", "storage", "bags"]),
            ],
            "Containers": [
                ("Storage Containers Set 10pc", 39.00, 29.00, ["containers", "storage", "set"]),
                ("Pantry Containers 8pc", 49.00, 39.00, ["pantry", "containers", "airtight"]),
                ("Under Bed Storage Box", 29.00, 24.00, ["under-bed", "storage", "box"]),
                ("Stackable Storage Bins 4pc", 39.00, 29.00, ["bins", "stackable", "storage"]),
            ],
        },
    },
    "APPAREL": {
        "Women": {
            "Tops": [
                ("Luxe Merino Wool Cardigan", 129.00, 129.00, ["cardigan", "wool", "premium", "winter"]),
                ("Silk Blend Blouse", 89.00, 79.00, ["blouse", "silk", "elegant"]),
                ("Cotton T-Shirt Basic", 29.00, 24.00, ["t-shirt", "cotton", "basic"]),
                ("Cashmere Sweater", 199.00, 179.00, ["sweater", "cashmere", "luxury"]),
                ("Denim Jacket Classic", 99.00, 89.00, ["jacket", "denim", "classic"]),
                ("Puffer Vest Lightweight", 79.00, 69.00, ["vest", "puffer", "lightweight"]),
                ("Linen Shirt Summer", 69.00, 59.00, ["shirt", "linen", "summer"]),
                ("Hoodie Oversized", 59.00, 49.00, ["hoodie", "oversized", "casual"]),
            ],
            "Bottoms": [
                ("High Waist Jeans Straight", 89.00, 79.00, ["jeans", "high-waist", "straight"]),
                ("Yoga Pants High Rise", 59.00, 49.00, ["yoga", "pants", "activewear"]),
                ("Linen Pants Wide Leg", 79.00, 69.00, ["pants", "linen", "wide-leg"]),
                ("Pencil Skirt Midi", 59.00, 49.00, ["skirt", "midi", "office"]),
                ("Shorts Denim High Rise", 49.00, 39.00, ["shorts", "denim", "summer"]),
                ("Leggings Full Length", 39.00, 29.00, ["leggings", "everyday", "comfort"]),
            ],
            "Dresses": [
                ("Maxi Dress Floral", 99.00, 89.00, ["dress", "maxi", "floral", "summer"]),
                ("Wrap Dress Office", 89.00, 79.00, ["dress", "wrap", "office"]),
                ("Little Black Dress", 79.00, 69.00, ["dress", "black", "classic"]),
                ("Casual Sundress", 59.00, 49.00, ["dress", "sundress", "casual"]),
                ("Evening Gown Formal", 199.00, 179.00, ["gown", "formal", "evening"]),
            ],
            "Outerwear": [
                ("Trench Coat Classic", 199.00, 179.00, ["coat", "trench", "classic"]),
                ("Parka Winter Long", 249.00, 219.00, ["parka", "winter", "warm"]),
                ("Leather Jacket Biker", 299.00, 269.00, ["jacket", "leather", "biker"]),
                ("Blazer Tailored", 149.00, 129.00, ["blazer", "tailored", "office"]),
            ],
        },
        "Men": {
            "Tops": [
                ("Oxford Shirt Classic", 79.00, 69.00, ["shirt", "oxford", "classic"]),
                ("Polo Shirt Cotton", 49.00, 39.00, ["polo", "cotton", "casual"]),
                ("Merino Wool Jumper", 129.00, 109.00, ["jumper", "merino", "winter"]),
                ("Plain T-Shirt 3 Pack", 49.00, 39.00, ["t-shirt", "pack", "basic"]),
                ("Flannel Shirt Check", 69.00, 59.00, ["shirt", "flannel", "casual"]),
                ("Henley Long Sleeve", 49.00, 39.00, ["henley", "long-sleeve", "casual"]),
                ("Linen Shirt Summer", 79.00, 69.00, ["shirt", "linen", "summer"]),
            ],
            "Bottoms": [
                ("Chinos Slim Fit", 79.00, 69.00, ["chinos", "slim", "smart-casual"]),
                ("Jeans Straight Leg", 89.00, 79.00, ["jeans", "straight", "classic"]),
                ("Shorts Cargo", 49.00, 39.00, ["shorts", "cargo", "casual"]),
                ("Track Pants Jogger", 59.00, 49.00, ["track-pants", "jogger", "comfort"]),
                ("Dress Pants Wool Blend", 99.00, 89.00, ["pants", "dress", "office"]),
            ],
            "Outerwear": [
                ("Bomber Jacket", 149.00, 129.00, ["jacket", "bomber", "casual"]),
                ("Puffer Jacket Hooded", 179.00, 159.00, ["jacket", "puffer", "warm"]),
                ("Wool Coat Long", 299.00, 269.00, ["coat", "wool", "formal"]),
                ("Denim Jacket Classic", 99.00, 89.00, ["jacket", "denim", "classic"]),
                ("Rain Jacket Waterproof", 129.00, 109.00, ["jacket", "rain", "waterproof"]),
            ],
            "Suits": [
                ("Two Piece Suit Navy", 349.00, 299.00, ["suit", "navy", "formal"]),
                ("Blazer Sport Coat", 199.00, 179.00, ["blazer", "sport-coat", "smart"]),
                ("Dress Shirt White", 69.00, 59.00, ["shirt", "dress", "formal"]),
                ("Tie Silk Patterned", 49.00, 39.00, ["tie", "silk", "formal"]),
            ],
        },
        "Kids": {
            "Boys": [
                ("Boys T-Shirt Graphic", 19.00, 14.00, ["t-shirt", "boys", "graphic"]),
                ("Boys Jeans Slim", 39.00, 29.00, ["jeans", "boys", "slim"]),
                ("Boys Hoodie Fleece", 39.00, 29.00, ["hoodie", "boys", "fleece"]),
                ("Boys Shorts Pack 2", 29.00, 24.00, ["shorts", "boys", "pack"]),
                ("Boys School Uniform Shirt", 24.00, 19.00, ["shirt", "school", "uniform"]),
            ],
            "Girls": [
                ("Girls Dress Floral", 39.00, 29.00, ["dress", "girls", "floral"]),
                ("Girls Leggings 2 Pack", 24.00, 19.00, ["leggings", "girls", "pack"]),
                ("Girls Cardigan Knit", 39.00, 29.00, ["cardigan", "girls", "knit"]),
                ("Girls T-Shirt Pack 3", 29.00, 24.00, ["t-shirt", "girls", "pack"]),
                ("Girls Skirt Tulle", 29.00, 24.00, ["skirt", "girls", "tulle"]),
            ],
            "School": [
                ("School Backpack Large", 49.00, 39.00, ["backpack", "school", "large"]),
                ("School Shoes Black", 59.00, 49.00, ["shoes", "school", "black"]),
                ("Lunchbox Insulated", 24.00, 19.00, ["lunchbox", "school", "insulated"]),
                ("School Socks 5 Pack", 19.00, 14.00, ["socks", "school", "pack"]),
            ],
        },
        "Baby": {
            "Clothing": [
                ("Baby Onesie 5 Pack", 29.00, 24.00, ["onesie", "baby", "pack"]),
                ("Baby Romper", 19.00, 14.00, ["romper", "baby", "cute"]),
                ("Baby Sleep Suit 3 Pack", 29.00, 24.00, ["sleep-suit", "baby", "pack"]),
                ("Baby Cardigan Knit", 24.00, 19.00, ["cardigan", "baby", "knit"]),
            ],
            "Accessories": [
                ("Baby Bib Set 5pc", 14.00, 9.00, ["bibs", "baby", "set"]),
                ("Baby Beanie", 9.00, 7.00, ["beanie", "baby", "warm"]),
                ("Baby Socks 6 Pack", 14.00, 9.00, ["socks", "baby", "pack"]),
            ],
        },
        "Footwear": {
            "Casual": [
                ("Sneakers Canvas", 59.00, 49.00, ["sneakers", "canvas", "casual"]),
                ("Slip-On Loafers", 79.00, 69.00, ["loafers", "slip-on", "comfort"]),
                ("Sandals Summer", 39.00, 29.00, ["sandals", "summer", "casual"]),
                ("Thongs Basic", 14.00, 9.00, ["thongs", "basic", "beach"]),
            ],
            "Sports": [
                ("Running Shoes Lightweight", 129.00, 109.00, ["running", "shoes", "lightweight"]),
                ("Training Shoes Cross", 99.00, 89.00, ["training", "shoes", "gym"]),
                ("Basketball Shoes High Top", 149.00, 129.00, ["basketball", "shoes", "high-top"]),
            ],
            "Formal": [
                ("Oxford Shoes Leather", 149.00, 129.00, ["oxford", "leather", "formal"]),
                ("Derby Shoes Brown", 129.00, 109.00, ["derby", "brown", "smart"]),
                ("Heels Classic Pump", 99.00, 89.00, ["heels", "pump", "formal"]),
            ],
            "Boots": [
                ("Ankle Boots Chelsea", 129.00, 109.00, ["boots", "chelsea", "ankle"]),
                ("Work Boots Steel Cap", 149.00, 129.00, ["boots", "work", "steel-cap"]),
                ("Hiking Boots Waterproof", 179.00, 159.00, ["boots", "hiking", "waterproof"]),
                ("Ugg Boots Classic", 149.00, 129.00, ["ugg", "boots", "warm"]),
            ],
        },
        "Accessories": {
            "Bags": [
                ("Tote Bag Leather", 149.00, 129.00, ["tote", "leather", "bag"]),
                ("Crossbody Bag", 79.00, 69.00, ["crossbody", "bag", "small"]),
                ("Backpack Urban", 99.00, 89.00, ["backpack", "urban", "style"]),
                ("Weekender Bag", 129.00, 109.00, ["weekender", "bag", "travel"]),
            ],
            "Jewelry": [
                ("Necklace Gold Plated", 39.00, 29.00, ["necklace", "gold", "jewelry"]),
                ("Earrings Stud Set", 24.00, 19.00, ["earrings", "stud", "set"]),
                ("Bracelet Charm", 29.00, 24.00, ["bracelet", "charm", "jewelry"]),
                ("Watch Analog Classic", 79.00, 69.00, ["watch", "analog", "classic"]),
            ],
            "Other": [
                ("Sunglasses Polarized", 49.00, 39.00, ["sunglasses", "polarized", "uv"]),
                ("Belt Leather", 39.00, 29.00, ["belt", "leather", "classic"]),
                ("Scarf Wool", 49.00, 39.00, ["scarf", "wool", "winter"]),
                ("Hat Fedora", 39.00, 29.00, ["hat", "fedora", "style"]),
                ("Umbrella Compact", 24.00, 19.00, ["umbrella", "compact", "rain"]),
            ],
        },
        "Activewear": {
            "Tops": [
                ("Sports Bra High Impact", 49.00, 39.00, ["sports-bra", "high-impact", "support"]),
                ("Tank Top Performance", 29.00, 24.00, ["tank-top", "performance", "breathable"]),
                ("Long Sleeve Running Top", 49.00, 39.00, ["running", "long-sleeve", "reflective"]),
            ],
            "Bottoms": [
                ("Running Shorts Lined", 39.00, 29.00, ["shorts", "running", "lined"]),
                ("Compression Tights", 59.00, 49.00, ["tights", "compression", "recovery"]),
                ("Yoga Leggings Pocket", 49.00, 39.00, ["leggings", "yoga", "pocket"]),
            ],
            "Sets": [
                ("Matching Gym Set 2pc", 79.00, 69.00, ["gym-set", "matching", "workout"]),
                ("Track Suit Full", 99.00, 89.00, ["tracksuit", "full", "athletic"]),
            ],
        },
    },
    "OUTDOOR_HARDWARE": {
        "Garden": {
            "Watering": [
                ("Smart Garden Irrigation System", 249.00, 199.00, ["irrigation", "smart", "wifi", "garden"]),
                ("Garden Hose 30m", 79.00, 69.00, ["hose", "garden", "30m"]),
                ("Sprinkler Oscillating", 39.00, 29.00, ["sprinkler", "oscillating", "lawn"]),
                ("Hose Reel Wall Mount", 99.00, 89.00, ["hose-reel", "wall-mount", "storage"]),
                ("Watering Can 10L", 24.00, 19.00, ["watering-can", "garden", "10l"]),
            ],
            "Tools": [
                ("Garden Tool Set 5pc", 49.00, 39.00, ["tools", "garden", "set"]),
                ("Pruning Shears Bypass", 29.00, 24.00, ["pruning", "shears", "garden"]),
                ("Hedge Trimmer Electric", 129.00, 109.00, ["hedge-trimmer", "electric", "garden"]),
                ("Lawn Edger", 79.00, 69.00, ["edger", "lawn", "garden"]),
                ("Wheelbarrow Steel", 149.00, 129.00, ["wheelbarrow", "steel", "heavy-duty"]),
            ],
            "Lawn Care": [
                ("Lawn Mower Electric", 399.00, 349.00, ["lawn-mower", "electric", "cordless"]),
                ("Lawn Mower Robot", 999.00, 899.00, ["lawn-mower", "robot", "smart"]),
                ("Leaf Blower Cordless", 179.00, 159.00, ["leaf-blower", "cordless", "powerful"]),
                ("Grass Seed 5kg", 49.00, 39.00, ["grass-seed", "lawn", "5kg"]),
                ("Fertilizer Lawn 10kg", 39.00, 29.00, ["fertilizer", "lawn", "10kg"]),
            ],
            "Pots & Planters": [
                ("Planter Box Raised Garden", 149.00, 129.00, ["planter", "raised", "garden"]),
                ("Pot Set Terracotta 3pc", 49.00, 39.00, ["pots", "terracotta", "set"]),
                ("Hanging Basket Set 2pc", 29.00, 24.00, ["hanging", "basket", "set"]),
                ("Self Watering Pot Large", 39.00, 29.00, ["pot", "self-watering", "large"]),
            ],
        },
        "Tools": {
            "Power Tools": [
                ("18V Brushless Drill Driver Kit", 199.00, 169.00, ["drill", "brushless", "18v", "kit"]),
                ("Circular Saw 185mm", 179.00, 159.00, ["circular-saw", "185mm", "power"]),
                ("Jigsaw Variable Speed", 129.00, 109.00, ["jigsaw", "variable-speed", "cutting"]),
                ("Angle Grinder 125mm", 99.00, 89.00, ["angle-grinder", "125mm", "metal"]),
                ("Impact Driver 18V", 149.00, 129.00, ["impact-driver", "18v", "powerful"]),
                ("Router Plunge", 199.00, 179.00, ["router", "plunge", "woodwork"]),
                ("Sander Orbital", 89.00, 79.00, ["sander", "orbital", "finishing"]),
                ("Multi Tool Oscillating", 149.00, 129.00, ["multi-tool", "oscillating", "versatile"]),
            ],
            "Hand Tools": [
                ("Socket Set 150pc", 149.00, 129.00, ["socket-set", "150pc", "comprehensive"]),
                ("Screwdriver Set 20pc", 39.00, 29.00, ["screwdriver", "set", "20pc"]),
                ("Hammer Claw 16oz", 29.00, 24.00, ["hammer", "claw", "16oz"]),
                ("Tape Measure 8m", 19.00, 14.00, ["tape-measure", "8m", "measuring"]),
                ("Level Spirit 600mm", 29.00, 24.00, ["level", "spirit", "600mm"]),
                ("Pliers Set 3pc", 29.00, 24.00, ["pliers", "set", "3pc"]),
                ("Adjustable Wrench Set", 39.00, 29.00, ["wrench", "adjustable", "set"]),
            ],
            "Tool Storage": [
                ("Tool Box Large", 79.00, 69.00, ["toolbox", "large", "storage"]),
                ("Tool Chest Rolling", 299.00, 269.00, ["tool-chest", "rolling", "workshop"]),
                ("Tool Belt Heavy Duty", 49.00, 39.00, ["tool-belt", "heavy-duty", "work"]),
                ("Pegboard Kit", 49.00, 39.00, ["pegboard", "kit", "organization"]),
            ],
        },
        "Outdoor Living": {
            "Furniture": [
                ("Outdoor Dining Set 7pc", 799.00, 699.00, ["outdoor-dining", "set", "7pc"]),
                ("Sun Lounger Pair", 299.00, 269.00, ["sun-lounger", "pair", "poolside"]),
                ("Hammock with Stand", 199.00, 179.00, ["hammock", "stand", "relaxation"]),
                ("Outdoor Sofa 3-Seater", 599.00, 549.00, ["outdoor-sofa", "3-seater", "patio"]),
                ("Outdoor Bar Setting", 449.00, 399.00, ["bar-setting", "outdoor", "entertaining"]),
            ],
            "BBQ": [
                ("Gas BBQ 4 Burner", 599.00, 549.00, ["bbq", "gas", "4-burner"]),
                ("Charcoal BBQ Kettle", 199.00, 179.00, ["bbq", "charcoal", "kettle"]),
                ("BBQ Tool Set 18pc", 79.00, 69.00, ["bbq-tools", "set", "18pc"]),
                ("BBQ Cover Large", 49.00, 39.00, ["bbq-cover", "large", "protective"]),
                ("Smoker Electric", 349.00, 299.00, ["smoker", "electric", "smoking"]),
            ],
            "Shade": [
                ("Cantilever Umbrella 3m", 299.00, 269.00, ["umbrella", "cantilever", "3m"]),
                ("Gazebo Pop Up 3x3m", 199.00, 179.00, ["gazebo", "pop-up", "3x3m"]),
                ("Shade Sail Triangle 5m", 149.00, 129.00, ["shade-sail", "triangle", "5m"]),
            ],
        },
        "Automotive": {
            "Car Care": [
                ("Car Vacuum Handheld", 79.00, 69.00, ["car-vacuum", "handheld", "portable"]),
                ("Pressure Washer Electric", 299.00, 269.00, ["pressure-washer", "electric", "cleaning"]),
                ("Car Wash Kit Complete", 49.00, 39.00, ["car-wash", "kit", "cleaning"]),
                ("Dash Cam 4K", 149.00, 129.00, ["dash-cam", "4k", "recording"]),
            ],
            "Accessories": [
                ("Car Phone Mount", 29.00, 24.00, ["car-mount", "phone", "magnetic"]),
                ("Car Seat Covers Set", 79.00, 69.00, ["seat-covers", "set", "protection"]),
                ("Floor Mats Rubber Set", 59.00, 49.00, ["floor-mats", "rubber", "all-weather"]),
                ("Boot Liner Universal", 49.00, 39.00, ["boot-liner", "universal", "protective"]),
            ],
            "Tools": [
                ("Jump Starter Portable", 129.00, 109.00, ["jump-starter", "portable", "battery"]),
                ("Tyre Inflator Digital", 79.00, 69.00, ["tyre-inflator", "digital", "portable"]),
                ("Jack Trolley 2 Tonne", 99.00, 89.00, ["jack", "trolley", "2-tonne"]),
            ],
        },
        "Camping": {
            "Tents": [
                ("Tent 4 Person Dome", 199.00, 179.00, ["tent", "4-person", "dome"]),
                ("Tent 6 Person Family", 349.00, 299.00, ["tent", "6-person", "family"]),
                ("Swag Single Canvas", 249.00, 219.00, ["swag", "single", "canvas"]),
                ("Tent 2 Person Lightweight", 129.00, 109.00, ["tent", "2-person", "hiking"]),
            ],
            "Sleeping": [
                ("Sleeping Bag -5C", 99.00, 89.00, ["sleeping-bag", "-5c", "warm"]),
                ("Sleeping Mat Self Inflating", 79.00, 69.00, ["sleeping-mat", "self-inflating", "comfort"]),
                ("Air Mattress Double", 89.00, 79.00, ["air-mattress", "double", "camping"]),
                ("Camping Pillow Compact", 24.00, 19.00, ["pillow", "camping", "compact"]),
            ],
            "Cooking": [
                ("Camping Stove 2 Burner", 99.00, 89.00, ["stove", "camping", "2-burner"]),
                ("Cooler Box 50L", 129.00, 109.00, ["cooler", "50l", "ice-box"]),
                ("Camping Cookware Set", 79.00, 69.00, ["cookware", "camping", "set"]),
                ("Water Container 20L", 29.00, 24.00, ["water-container", "20l", "camping"]),
            ],
            "Furniture": [
                ("Camping Chair Folding", 49.00, 39.00, ["chair", "camping", "folding"]),
                ("Camping Table Folding", 79.00, 69.00, ["table", "camping", "folding"]),
                ("Camp Bed Stretcher", 99.00, 89.00, ["camp-bed", "stretcher", "elevated"]),
            ],
        },
        "Sports": {
            "Fitness": [
                ("Dumbbell Set Adjustable", 299.00, 269.00, ["dumbbells", "adjustable", "home-gym"]),
                ("Yoga Mat Premium", 49.00, 39.00, ["yoga-mat", "premium", "non-slip"]),
                ("Resistance Bands Set", 29.00, 24.00, ["resistance-bands", "set", "exercise"]),
                ("Kettlebell 12kg", 59.00, 49.00, ["kettlebell", "12kg", "strength"]),
                ("Pull Up Bar Door", 39.00, 29.00, ["pull-up-bar", "door", "strength"]),
                ("Exercise Bike Spin", 499.00, 449.00, ["exercise-bike", "spin", "cardio"]),
                ("Treadmill Folding", 799.00, 699.00, ["treadmill", "folding", "home"]),
            ],
            "Cycling": [
                ("Bicycle Helmet Adult", 79.00, 69.00, ["helmet", "bicycle", "adult"]),
                ("Bike Lock Heavy Duty", 49.00, 39.00, ["bike-lock", "heavy-duty", "security"]),
                ("Cycling Gloves", 29.00, 24.00, ["gloves", "cycling", "padded"]),
                ("Bike Lights Set", 39.00, 29.00, ["bike-lights", "set", "safety"]),
            ],
            "Water Sports": [
                ("Snorkel Set Adult", 59.00, 49.00, ["snorkel", "set", "adult"]),
                ("Inflatable SUP Board", 499.00, 449.00, ["sup", "inflatable", "paddleboard"]),
                ("Pool Float Inflatable", 29.00, 24.00, ["pool-float", "inflatable", "fun"]),
                ("Swim Goggles Adult", 24.00, 19.00, ["goggles", "swim", "adult"]),
            ],
            "Ball Sports": [
                ("Soccer Ball Size 5", 29.00, 24.00, ["soccer-ball", "size-5", "official"]),
                ("Basketball Official", 39.00, 29.00, ["basketball", "official", "indoor-outdoor"]),
                ("Tennis Racket Adult", 79.00, 69.00, ["tennis", "racket", "adult"]),
                ("Cricket Set Complete", 99.00, 89.00, ["cricket", "set", "complete"]),
            ],
        },
    },
    "OFFICE_TECH": {
        "Computers": {
            "Laptops": [
                ("UltraBook Pro 15\" Laptop", 1499.00, 1299.00, ["laptop", "ultrabook", "15-inch", "premium"]),
                ("Gaming Laptop 17\"", 1999.00, 1799.00, ["laptop", "gaming", "17-inch", "powerful"]),
                ("Budget Laptop 14\"", 599.00, 549.00, ["laptop", "budget", "14-inch", "basic"]),
                ("2-in-1 Convertible Laptop", 1099.00, 999.00, ["laptop", "2-in-1", "convertible", "touch"]),
                ("Business Laptop 15\"", 1299.00, 1199.00, ["laptop", "business", "professional"]),
            ],
            "Desktops": [
                ("Desktop PC Tower", 899.00, 799.00, ["desktop", "tower", "pc"]),
                ("All-in-One PC 27\"", 1299.00, 1199.00, ["all-in-one", "27-inch", "desktop"]),
                ("Mini PC Compact", 499.00, 449.00, ["mini-pc", "compact", "space-saving"]),
                ("Gaming Desktop RTX", 2499.00, 2299.00, ["desktop", "gaming", "rtx", "powerful"]),
            ],
            "Tablets": [
                ("Tablet 10\" WiFi", 449.00, 399.00, ["tablet", "10-inch", "wifi"]),
                ("Tablet Pro 12\"", 899.00, 799.00, ["tablet", "pro", "12-inch", "stylus"]),
                ("Kids Tablet 8\"", 199.00, 179.00, ["tablet", "kids", "8-inch", "safe"]),
            ],
        },
        "Monitors": {
            "Work": [
                ("Monitor 27\" 4K IPS", 499.00, 449.00, ["monitor", "27-inch", "4k", "ips"]),
                ("Monitor 24\" FHD", 249.00, 219.00, ["monitor", "24-inch", "fhd"]),
                ("Ultrawide Monitor 34\"", 699.00, 629.00, ["monitor", "ultrawide", "34-inch"]),
                ("Portable Monitor 15.6\"", 299.00, 269.00, ["monitor", "portable", "15.6-inch"]),
            ],
            "Gaming": [
                ("Gaming Monitor 27\" 165Hz", 449.00, 399.00, ["monitor", "gaming", "165hz"]),
                ("Gaming Monitor 32\" Curved", 599.00, 549.00, ["monitor", "gaming", "curved", "32-inch"]),
            ],
        },
        "Printers": {
            "Inkjet": [
                ("Inkjet Printer All-in-One", 149.00, 129.00, ["printer", "inkjet", "all-in-one"]),
                ("Photo Printer 6x4", 99.00, 89.00, ["printer", "photo", "compact"]),
            ],
            "Laser": [
                ("Laser Printer Mono", 199.00, 179.00, ["printer", "laser", "mono", "fast"]),
                ("Laser Printer Color", 399.00, 349.00, ["printer", "laser", "color"]),
            ],
            "Supplies": [
                ("Ink Cartridges Multi-Pack", 79.00, 69.00, ["ink", "cartridges", "multi-pack"]),
                ("Toner Cartridge Black", 89.00, 79.00, ["toner", "black", "laser"]),
                ("Photo Paper Glossy 100pk", 29.00, 24.00, ["photo-paper", "glossy", "100-pack"]),
            ],
        },
        "Office Supplies": {
            "Paper": [
                ("Copy Paper A4 5 Ream", 39.00, 29.00, ["paper", "a4", "5-ream"]),
                ("Notebook Spiral A4 5pk", 19.00, 14.00, ["notebook", "spiral", "5-pack"]),
                ("Sticky Notes Pack", 14.00, 9.00, ["sticky-notes", "pack", "assorted"]),
            ],
            "Writing": [
                ("Pen Set Blue 12pk", 9.00, 7.00, ["pens", "blue", "12-pack"]),
                ("Highlighters 6 Pack", 9.00, 7.00, ["highlighters", "6-pack", "assorted"]),
                ("Whiteboard Markers 4pk", 14.00, 9.00, ["whiteboard", "markers", "4-pack"]),
            ],
            "Organization": [
                ("Desk Organizer Set", 29.00, 24.00, ["desk-organizer", "set", "tidy"]),
                ("File Folders 50pk", 19.00, 14.00, ["file-folders", "50-pack", "organization"]),
                ("Binder Clips Assorted", 9.00, 7.00, ["binder-clips", "assorted", "office"]),
            ],
        },
        "Tech Accessories": {
            "Storage": [
                ("USB Flash Drive 64GB", 19.00, 14.00, ["usb", "flash-drive", "64gb"]),
                ("External SSD 1TB", 149.00, 129.00, ["ssd", "external", "1tb", "fast"]),
                ("External HDD 2TB", 99.00, 89.00, ["hdd", "external", "2tb", "backup"]),
                ("Memory Card SD 256GB", 49.00, 39.00, ["memory-card", "sd", "256gb"]),
            ],
            "Cables": [
                ("USB-C Cable 2m", 19.00, 14.00, ["cable", "usb-c", "2m"]),
                ("HDMI Cable 3m", 24.00, 19.00, ["cable", "hdmi", "3m"]),
                ("Extension Cord 4 Way", 29.00, 24.00, ["extension", "power", "4-way"]),
            ],
            "Input Devices": [
                ("Wireless Mouse", 39.00, 29.00, ["mouse", "wireless", "ergonomic"]),
                ("Wireless Keyboard", 59.00, 49.00, ["keyboard", "wireless", "quiet"]),
                ("Keyboard Mouse Combo", 79.00, 69.00, ["keyboard", "mouse", "combo"]),
                ("Webcam HD 1080p", 79.00, 69.00, ["webcam", "hd", "1080p"]),
            ],
        },
        "Furniture": {
            "Desks": [
                ("Standing Desk Electric Adjustable", 699.00, 599.00, ["standing-desk", "electric", "adjustable"]),
                ("Computer Desk Large", 299.00, 269.00, ["desk", "computer", "large"]),
                ("Corner Desk L-Shape", 349.00, 299.00, ["desk", "corner", "l-shape"]),
            ],
            "Chairs": [
                ("Office Chair Ergonomic Mesh", 449.00, 399.00, ["chair", "ergonomic", "mesh"]),
                ("Executive Chair Leather", 599.00, 549.00, ["chair", "executive", "leather"]),
                ("Budget Office Chair", 149.00, 129.00, ["chair", "budget", "office"]),
            ],
            "Accessories": [
                ("Monitor Stand Riser", 49.00, 39.00, ["monitor-stand", "riser", "ergonomic"]),
                ("Laptop Stand Adjustable", 59.00, 49.00, ["laptop-stand", "adjustable", "portable"]),
                ("Footrest Ergonomic", 49.00, 39.00, ["footrest", "ergonomic", "comfort"]),
            ],
        },
    },
    "TOYS_ENTERTAINMENT": {
        "Toys": {
            "Action Figures": [
                ("Action Figure Superhero", 29.00, 24.00, ["action-figure", "superhero", "collectible"]),
                ("Action Figure Set 4pc", 49.00, 39.00, ["action-figures", "set", "4-pack"]),
                ("Robot Transformer Toy", 39.00, 29.00, ["robot", "transformer", "toy"]),
            ],
            "Building": [
                ("Building Blocks 500pc", 49.00, 39.00, ["building-blocks", "500pc", "creative"]),
                ("Building Set City Theme", 79.00, 69.00, ["building-set", "city", "theme"]),
                ("Magnetic Tiles 100pc", 69.00, 59.00, ["magnetic-tiles", "100pc", "stem"]),
            ],
            "Dolls": [
                ("Fashion Doll Deluxe", 39.00, 29.00, ["doll", "fashion", "accessories"]),
                ("Baby Doll Interactive", 49.00, 39.00, ["doll", "baby", "interactive"]),
                ("Dollhouse Wooden", 149.00, 129.00, ["dollhouse", "wooden", "play"]),
            ],
            "Vehicles": [
                ("Remote Control Car", 59.00, 49.00, ["rc-car", "remote-control", "fast"]),
                ("Train Set Electric", 99.00, 89.00, ["train-set", "electric", "classic"]),
                ("Die Cast Cars 10 Pack", 29.00, 24.00, ["die-cast", "cars", "10-pack"]),
            ],
            "Outdoor": [
                ("Trampoline 10ft", 399.00, 349.00, ["trampoline", "10ft", "outdoor"]),
                ("Swing Set Double", 299.00, 269.00, ["swing-set", "double", "outdoor"]),
                ("Cubby House Wooden", 499.00, 449.00, ["cubby-house", "wooden", "play"]),
                ("Sandpit with Cover", 129.00, 109.00, ["sandpit", "cover", "play"]),
            ],
        },
        "Games": {
            "Board Games": [
                ("Family Board Game Classic", 39.00, 29.00, ["board-game", "family", "classic"]),
                ("Strategy Board Game", 59.00, 49.00, ["board-game", "strategy", "adult"]),
                ("Kids Board Game Simple", 24.00, 19.00, ["board-game", "kids", "simple"]),
                ("Party Game Cards", 29.00, 24.00, ["party-game", "cards", "fun"]),
            ],
            "Puzzles": [
                ("Jigsaw Puzzle 1000pc", 29.00, 24.00, ["puzzle", "jigsaw", "1000pc"]),
                ("Jigsaw Puzzle 500pc", 19.00, 14.00, ["puzzle", "jigsaw", "500pc"]),
                ("3D Puzzle Building", 39.00, 29.00, ["puzzle", "3d", "building"]),
                ("Kids Puzzle 100pc", 14.00, 9.00, ["puzzle", "kids", "100pc"]),
            ],
            "Video Games": [
                ("Video Game Action Adventure", 79.00, 69.00, ["video-game", "action", "adventure"]),
                ("Video Game Sports", 79.00, 69.00, ["video-game", "sports", "simulation"]),
                ("Video Game Family", 59.00, 49.00, ["video-game", "family", "party"]),
                ("Video Game Racing", 69.00, 59.00, ["video-game", "racing", "cars"]),
            ],
        },
        "Arts & Crafts": {
            "Drawing": [
                ("Art Set Complete 150pc", 49.00, 39.00, ["art-set", "complete", "150pc"]),
                ("Coloring Pencils 72pc", 29.00, 24.00, ["pencils", "coloring", "72pc"]),
                ("Sketch Pad A3", 14.00, 9.00, ["sketch-pad", "a3", "drawing"]),
                ("Markers Washable 24pk", 19.00, 14.00, ["markers", "washable", "24-pack"]),
            ],
            "Craft Kits": [
                ("Slime Making Kit", 24.00, 19.00, ["slime", "kit", "diy"]),
                ("Jewelry Making Kit", 29.00, 24.00, ["jewelry", "making", "kit"]),
                ("Sewing Kit Kids", 24.00, 19.00, ["sewing", "kit", "kids"]),
                ("Science Kit STEM", 39.00, 29.00, ["science", "kit", "stem"]),
            ],
        },
        "Party": {
            "Decorations": [
                ("Birthday Party Kit", 29.00, 24.00, ["birthday", "party", "kit"]),
                ("Balloon Pack 50pc", 14.00, 9.00, ["balloons", "50-pack", "assorted"]),
                ("Banner Happy Birthday", 9.00, 7.00, ["banner", "birthday", "decoration"]),
            ],
            "Supplies": [
                ("Party Plates 20 Pack", 9.00, 7.00, ["plates", "party", "20-pack"]),
                ("Party Cups 20 Pack", 9.00, 7.00, ["cups", "party", "20-pack"]),
                ("Napkins Party 40 Pack", 9.00, 7.00, ["napkins", "party", "40-pack"]),
                ("Party Bags 10 Pack", 9.00, 7.00, ["party-bags", "10-pack", "loot"]),
            ],
        },
    },
    "HEALTH_BEAUTY": {
        "Personal Care": {
            "Oral Care": [
                ("Electric Toothbrush Pro", 149.00, 129.00, ["toothbrush", "electric", "pro"]),
                ("Electric Toothbrush Basic", 49.00, 39.00, ["toothbrush", "electric", "basic"]),
                ("Water Flosser", 89.00, 79.00, ["water-flosser", "dental", "care"]),
                ("Toothpaste Whitening 3pk", 19.00, 14.00, ["toothpaste", "whitening", "3-pack"]),
            ],
            "Hair Removal": [
                ("Electric Shaver Men", 129.00, 109.00, ["shaver", "electric", "men"]),
                ("Hair Trimmer Kit", 79.00, 69.00, ["trimmer", "hair", "kit"]),
                ("Epilator Women", 99.00, 89.00, ["epilator", "women", "hair-removal"]),
                ("IPL Hair Removal Device", 299.00, 269.00, ["ipl", "hair-removal", "permanent"]),
            ],
            "Bath & Body": [
                ("Body Wash Set 3pc", 24.00, 19.00, ["body-wash", "set", "3-pack"]),
                ("Bath Bomb Gift Set", 29.00, 24.00, ["bath-bombs", "gift", "set"]),
                ("Body Lotion Premium", 19.00, 14.00, ["body-lotion", "premium", "moisturizing"]),
            ],
        },
        "Haircare": {
            "Styling Tools": [
                ("Hair Dryer Professional", 129.00, 109.00, ["hair-dryer", "professional", "powerful"]),
                ("Hair Straightener Ceramic", 99.00, 89.00, ["straightener", "ceramic", "hair"]),
                ("Curling Iron Wand", 79.00, 69.00, ["curling-iron", "wand", "styling"]),
                ("Hot Air Brush", 89.00, 79.00, ["hot-air-brush", "styling", "volume"]),
            ],
            "Products": [
                ("Shampoo & Conditioner Set", 29.00, 24.00, ["shampoo", "conditioner", "set"]),
                ("Hair Mask Treatment", 24.00, 19.00, ["hair-mask", "treatment", "repair"]),
                ("Hair Oil Argan", 19.00, 14.00, ["hair-oil", "argan", "nourishing"]),
            ],
        },
        "Skincare": {
            "Face Care": [
                ("Face Cleansing Device", 149.00, 129.00, ["face-cleansing", "device", "skin"]),
                ("Facial Serum Vitamin C", 39.00, 29.00, ["serum", "vitamin-c", "brightening"]),
                ("Moisturizer SPF 50", 29.00, 24.00, ["moisturizer", "spf50", "protection"]),
                ("Face Mask Sheet 10pk", 19.00, 14.00, ["face-mask", "sheet", "10-pack"]),
                ("Eye Cream Anti-Aging", 39.00, 29.00, ["eye-cream", "anti-aging", "wrinkles"]),
            ],
            "Body Care": [
                ("Body Scrub Exfoliating", 24.00, 19.00, ["body-scrub", "exfoliating", "smooth"]),
                ("Hand Cream Set", 19.00, 14.00, ["hand-cream", "set", "moisturizing"]),
                ("Sunscreen SPF 50+ 200ml", 24.00, 19.00, ["sunscreen", "spf50", "200ml"]),
            ],
        },
        "Cosmetics": {
            "Face": [
                ("Foundation Liquid", 39.00, 29.00, ["foundation", "liquid", "coverage"]),
                ("Concealer Duo", 24.00, 19.00, ["concealer", "duo", "brightening"]),
                ("Setting Powder", 29.00, 24.00, ["setting-powder", "matte", "long-lasting"]),
                ("Blush Palette", 29.00, 24.00, ["blush", "palette", "shades"]),
            ],
            "Eyes": [
                ("Eyeshadow Palette 12 Shade", 39.00, 29.00, ["eyeshadow", "palette", "12-shades"]),
                ("Mascara Volumizing", 24.00, 19.00, ["mascara", "volumizing", "black"]),
                ("Eyeliner Pen", 19.00, 14.00, ["eyeliner", "pen", "precise"]),
                ("False Lashes Kit", 19.00, 14.00, ["lashes", "false", "kit"]),
            ],
            "Lips": [
                ("Lipstick Set 6pc", 39.00, 29.00, ["lipstick", "set", "6-pack"]),
                ("Lip Gloss Plumping", 19.00, 14.00, ["lip-gloss", "plumping", "shine"]),
                ("Lip Balm SPF 15 3pk", 14.00, 9.00, ["lip-balm", "spf15", "3-pack"]),
            ],
            "Brushes": [
                ("Makeup Brush Set 12pc", 49.00, 39.00, ["makeup-brushes", "set", "12-pack"]),
                ("Beauty Blender Set", 19.00, 14.00, ["beauty-blender", "set", "application"]),
            ],
        },
        "Fitness": {
            "Supplements": [
                ("Protein Powder 1kg", 59.00, 49.00, ["protein", "powder", "1kg"]),
                ("Pre-Workout Supplement", 39.00, 29.00, ["pre-workout", "supplement", "energy"]),
                ("Multivitamin 90 Tablets", 29.00, 24.00, ["multivitamin", "90-tablets", "daily"]),
            ],
            "Equipment": [
                ("Foam Roller", 29.00, 24.00, ["foam-roller", "recovery", "massage"]),
                ("Massage Gun", 149.00, 129.00, ["massage-gun", "recovery", "muscle"]),
                ("Fitness Tracker Watch", 99.00, 89.00, ["fitness-tracker", "watch", "health"]),
            ],
        },
        "Health": {
            "First Aid": [
                ("First Aid Kit Complete", 49.00, 39.00, ["first-aid", "kit", "complete"]),
                ("Bandages Assorted Box", 14.00, 9.00, ["bandages", "assorted", "box"]),
                ("Thermometer Digital", 19.00, 14.00, ["thermometer", "digital", "fever"]),
            ],
            "Wellness": [
                ("Blood Pressure Monitor", 79.00, 69.00, ["blood-pressure", "monitor", "health"]),
                ("Pulse Oximeter", 39.00, 29.00, ["pulse-oximeter", "oxygen", "health"]),
                ("Heating Pad Electric", 49.00, 39.00, ["heating-pad", "electric", "pain-relief"]),
            ],
        },
    },
}

def generate_sku(division: str, category: str, index: int) -> str:
    prefix_map = {
        "ELECTRONICS": "EL",
        "HOME_LIVING": "HL",
        "APPAREL": "AP",
        "OUTDOOR_HARDWARE": "OH",
        "OFFICE_TECH": "OT",
        "TOYS_ENTERTAINMENT": "TE",
        "HEALTH_BEAUTY": "HB",
    }
    cat_prefix = category[:3].upper()
    prefix = prefix_map.get(division, "XX")
    return f"{prefix}-{cat_prefix}-{index:05d}"

def generate_products():
    products = []
    sku_counter = 10000
    
    supplier_map = {
        "ELECTRONICS": ["SUP-002", "SUP-007"],
        "HOME_LIVING": ["SUP-001", "SUP-006"],
        "APPAREL": ["SUP-003"],
        "OUTDOOR_HARDWARE": ["SUP-004", "SUP-005", "SUP-010"],
        "OFFICE_TECH": ["SUP-002"],
        "TOYS_ENTERTAINMENT": ["SUP-008"],
        "HEALTH_BEAUTY": ["SUP-009"],
    }
    
    colors = ["Black", "White", "Grey", "Navy", "Charcoal", "Silver", "Rose Gold", "Blue", "Red", "Green", "Beige", "Brown"]
    
    for division, categories in PRODUCT_CATALOG.items():
        division_brands = BRANDS.get(division, ["Generic"])
        suppliers = supplier_map.get(division, ["SUP-001"])
        
        for category, subcategories in categories.items():
            for subcategory, items in subcategories.items():
                for item in items:
                    name, base_price, current_price, tags = item
                    sku_counter += 1
                    
                    brand = random.choice(division_brands)
                    supplier_id = random.choice(suppliers)
                    color = random.choice(colors) if random.random() > 0.3 else None
                    
                    cost = round(current_price * random.uniform(0.35, 0.55), 2)
                    weight = round(random.uniform(0.1, 15.0), 2)
                    cube = round(random.uniform(0.001, 0.5), 3)
                    lead_time = random.randint(10, 50)
                    reorder = random.randint(50, 500)
                    safety = random.randint(20, 150)
                    
                    product = {
                        "sku": generate_sku(division, category, sku_counter),
                        "name": name,
                        "division": division,
                        "category": category,
                        "subcategory": subcategory,
                        "brand": brand,
                        "supplier_id": supplier_id,
                        "base_price": base_price,
                        "current_price": current_price,
                        "cost": cost,
                        "weight_kg": weight,
                        "cube_m3": cube,
                        "lead_time_days": lead_time,
                        "reorder_point": reorder,
                        "safety_stock": safety,
                        "pack_size": 1,
                        "tags": tags + [category.lower().replace(" ", "-"), subcategory.lower().replace(" ", "-")],
                    }
                    
                    if color:
                        product["attributes"] = {"color": color}
                    
                    products.append(product)
    
    return products

PRODUCTS = generate_products()

STORES = [
    {"id": "STR-SYD-001", "name": "Sydney CBD Flagship", "state": "NSW", "suburb": "Sydney", "lat": -33.8688, "lng": 151.2093, "dc": "SYD-DC-01", "format": "Flagship", "sqm": 12000, "staff": 185},
    {"id": "STR-SYD-002", "name": "Bondi Junction", "state": "NSW", "suburb": "Bondi Junction", "lat": -33.8914, "lng": 151.2476, "dc": "SYD-DC-01", "format": "Large", "sqm": 6500, "staff": 92},
    {"id": "STR-SYD-003", "name": "Parramatta Westfield", "state": "NSW", "suburb": "Parramatta", "lat": -33.8151, "lng": 151.0011, "dc": "SYD-DC-01", "format": "Large", "sqm": 5800, "staff": 78},
    {"id": "STR-SYD-004", "name": "Burwood Plaza", "state": "NSW", "suburb": "Burwood", "lat": -33.8773, "lng": 151.1045, "dc": "SYD-DC-01", "format": "Medium", "sqm": 3200, "staff": 45},
    {"id": "STR-MEL-001", "name": "Melbourne Central Flagship", "state": "VIC", "suburb": "Melbourne", "lat": -37.8136, "lng": 144.9631, "dc": "MEL-DC-02", "format": "Flagship", "sqm": 11000, "staff": 165},
    {"id": "STR-MEL-002", "name": "Chadstone", "state": "VIC", "suburb": "Chadstone", "lat": -37.8857, "lng": 145.0831, "dc": "MEL-DC-02", "format": "Large", "sqm": 7200, "staff": 105},
    {"id": "STR-MEL-003", "name": "Burwood East", "state": "VIC", "suburb": "Burwood East", "lat": -37.8500, "lng": 145.1500, "dc": "MEL-DC-02", "format": "Medium", "sqm": 4500, "staff": 62},
    {"id": "STR-MEL-004", "name": "Glen Waverley", "state": "VIC", "suburb": "Glen Waverley", "lat": -37.8781, "lng": 145.1647, "dc": "MEL-DC-02", "format": "Large", "sqm": 5200, "staff": 75},
    {"id": "STR-MEL-005", "name": "Box Hill", "state": "VIC", "suburb": "Box Hill", "lat": -37.8186, "lng": 145.1218, "dc": "MEL-DC-02", "format": "Medium", "sqm": 3800, "staff": 52},
    {"id": "STR-MEL-006", "name": "Doncaster", "state": "VIC", "suburb": "Doncaster", "lat": -37.7847, "lng": 145.1255, "dc": "MEL-DC-02", "format": "Large", "sqm": 5600, "staff": 82},
    {"id": "STR-MEL-007", "name": "Highpoint", "state": "VIC", "suburb": "Maribyrnong", "lat": -37.7728, "lng": 144.8889, "dc": "MEL-DC-02", "format": "Large", "sqm": 6100, "staff": 88},
    {"id": "STR-MEL-008", "name": "Knox Ozone", "state": "VIC", "suburb": "Wantirna South", "lat": -37.8683, "lng": 145.2428, "dc": "MEL-DC-02", "format": "Medium", "sqm": 4200, "staff": 58},
    {"id": "STR-BNE-001", "name": "Brisbane Queen Street", "state": "QLD", "suburb": "Brisbane", "lat": -27.4698, "lng": 153.0251, "dc": "BNE-DC-03", "format": "Flagship", "sqm": 9500, "staff": 142},
    {"id": "STR-BNE-002", "name": "Chermside", "state": "QLD", "suburb": "Chermside", "lat": -27.3859, "lng": 153.0309, "dc": "BNE-DC-03", "format": "Large", "sqm": 5800, "staff": 78},
    {"id": "STR-BNE-003", "name": "Garden City", "state": "QLD", "suburb": "Upper Mount Gravatt", "lat": -27.5539, "lng": 153.0762, "dc": "BNE-DC-03", "format": "Large", "sqm": 5500, "staff": 72},
    {"id": "STR-PER-001", "name": "Perth City Flagship", "state": "WA", "suburb": "Perth", "lat": -31.9505, "lng": 115.8605, "dc": "PER-DC-04", "format": "Flagship", "sqm": 8800, "staff": 128},
    {"id": "STR-PER-002", "name": "Carousel", "state": "WA", "suburb": "Cannington", "lat": -32.0174, "lng": 115.9381, "dc": "PER-DC-04", "format": "Large", "sqm": 5200, "staff": 68},
    {"id": "STR-ADL-001", "name": "Adelaide Rundle Mall", "state": "SA", "suburb": "Adelaide", "lat": -34.9285, "lng": 138.6007, "dc": "ADL-DC-05", "format": "Large", "sqm": 6200, "staff": 88},
    {"id": "STR-ADL-002", "name": "Tea Tree Plaza", "state": "SA", "suburb": "Modbury", "lat": -34.8329, "lng": 138.6825, "dc": "ADL-DC-05", "format": "Medium", "sqm": 4100, "staff": 55},
]

CUSTOMERS = [
    {
        "id": "CUST-00001",
        "name": "Alex Morgan",
        "email": "alex.morgan@email.com",
        "tier": "PLATINUM",
        "loyalty_points": 48500,
        "lifetime_value": 12850.00,
        "avg_basket": 185.00,
        "purchase_frequency": "weekly",
        "preferred_store": "STR-MEL-003",
        "preferred_channel": "online",
        "segments": ["high-value", "tech-enthusiast", "premium-buyer"],
        "free_delivery_remaining": 12
    },
    {
        "id": "CUST-00002",
        "name": "James Chen",
        "email": "james.chen@email.com",
        "tier": "GOLD",
        "loyalty_points": 22300,
        "lifetime_value": 5420.00,
        "avg_basket": 145.00,
        "purchase_frequency": "fortnightly",
        "preferred_store": "STR-MEL-001",
        "preferred_channel": "omni",
        "segments": ["tech-enthusiast", "price-conscious"],
        "free_delivery_remaining": 6
    },
    {
        "id": "CUST-00003",
        "name": "Emma Thompson",
        "email": "emma.t@email.com",
        "tier": "PLATINUM",
        "loyalty_points": 62100,
        "lifetime_value": 18920.00,
        "avg_basket": 220.00,
        "purchase_frequency": "weekly",
        "preferred_store": "STR-SYD-002",
        "preferred_channel": "in-store",
        "segments": ["home-decorator", "premium-buyer", "loyal"],
        "free_delivery_remaining": 24
    }
]

INVENTORY_BY_LOCATION = {}
for product in PRODUCTS[:50]:
    sku = product["sku"]
    INVENTORY_BY_LOCATION[sku] = {
        "SYD-DC-01": {"on_hand": random.randint(100, 500), "allocated": random.randint(10, 50), "in_transit": random.randint(50, 200), "atp": random.randint(80, 400)},
        "MEL-DC-02": {"on_hand": random.randint(80, 400), "allocated": random.randint(8, 40), "in_transit": random.randint(40, 150), "atp": random.randint(60, 350)},
    }

SHIPPING_ROUTES = [
    {"origin": "Shanghai", "port_destination": "Sydney", "transit_days": 18, "carrier": "Maersk", "vessel_frequency": "weekly"},
    {"origin": "Ho Chi Minh", "port_destination": "Melbourne", "transit_days": 14, "carrier": "CMA CGM", "vessel_frequency": "bi-weekly"},
    {"origin": "Bangkok", "port_destination": "Brisbane", "transit_days": 12, "carrier": "OOCL", "vessel_frequency": "weekly"},
    {"origin": "Kaohsiung", "port_destination": "Sydney", "transit_days": 16, "carrier": "Evergreen", "vessel_frequency": "weekly"},
    {"origin": "Shenzhen", "port_destination": "Melbourne", "transit_days": 15, "carrier": "COSCO", "vessel_frequency": "weekly"},
    {"origin": "Busan", "port_destination": "Sydney", "transit_days": 12, "carrier": "HMM", "vessel_frequency": "bi-weekly"},
    {"origin": "Guangzhou", "port_destination": "Brisbane", "transit_days": 14, "carrier": "Yang Ming", "vessel_frequency": "weekly"},
]

AGENT_DEFINITIONS = {
    "DEMAND_SENSING": {
        "name": "Demand Sensing Agent",
        "icon": "📊",
        "color": "#6366f1",
        "capabilities": ["real-time demand signal capture", "trend analysis", "seasonality detection", "promotional impact"],
        "data_sources": ["POS transactions", "web analytics", "social signals", "weather data"],
        "output": "Demand forecast adjustments"
    },
    "INVENTORY_OPTIMIZER": {
        "name": "Inventory Optimization Agent",
        "icon": "📦",
        "color": "#10b981",
        "capabilities": ["ATP calculation", "safety stock optimization", "reorder point management", "dead stock detection"],
        "data_sources": ["WMS", "ERP", "Supplier feeds", "DC capacity"],
        "output": "Inventory recommendations"
    },
    "FULFILLMENT_ORCHESTRATOR": {
        "name": "Fulfillment Orchestrator Agent",
        "icon": "🏭",
        "color": "#f59e0b",
        "capabilities": ["order routing", "pick optimization", "wave planning", "carrier selection"],
        "data_sources": ["OMS", "WMS", "TMS", "Store inventory"],
        "output": "Fulfillment instructions"
    },
    "SUPPLIER_COLLABORATION": {
        "name": "Supplier Collaboration Agent",
        "icon": "🤝",
        "color": "#ef4444",
        "capabilities": ["auto-PO generation", "lead time optimization", "supplier scoring", "risk monitoring"],
        "data_sources": ["SRM", "Contracts", "Performance metrics", "Market data"],
        "output": "Purchase orders & forecasts"
    },
    "LOGISTICS_OPTIMIZER": {
        "name": "Logistics Optimization Agent",
        "icon": "🚚",
        "color": "#8b5cf6",
        "capabilities": ["route optimization", "load planning", "carrier management", "track & trace"],
        "data_sources": ["TMS", "Carrier APIs", "Traffic data", "Weather"],
        "output": "Shipping plans & updates"
    },
    "PRICING_AGENT": {
        "name": "Dynamic Pricing Agent",
        "icon": "💰",
        "color": "#ec4899",
        "capabilities": ["competitive monitoring", "elasticity modeling", "markdown optimization", "promotion planning"],
        "data_sources": ["Competitor feeds", "Sales history", "Inventory levels", "Margin targets"],
        "output": "Price recommendations"
    },
    "CUSTOMER_INTELLIGENCE": {
        "name": "Customer Intelligence Agent",
        "icon": "👤",
        "color": "#14b8a6",
        "capabilities": ["segment analysis", "churn prediction", "CLV calculation", "personalization"],
        "data_sources": ["CRM", "Transaction history", "Web behavior", "Survey data"],
        "output": "Customer insights & actions"
    }
}

DEMO_SCENARIOS = [
    {
        "id": "SCENARIO-001",
        "name": "High-Value Customer Product Discovery",
        "description": "Platinum loyalty customer searching for premium home products",
        "customer_id": "CUST-00001",
        "query": "I'm looking for a quality sofa for my living room renovation",
        "expected_product": "HL-FRN-42891",
        "agents_involved": ["DEMAND_SENSING", "INVENTORY_OPTIMIZER", "CUSTOMER_INTELLIGENCE", "PRICING_AGENT"],
        "business_value": "Personalized experience drives 40% higher conversion"
    },
    {
        "id": "SCENARIO-002", 
        "name": "Stock Depletion & Auto-Replenishment",
        "description": "Popular electronics item triggers automated supply chain response",
        "customer_id": "CUST-00002",
        "query": "I need wireless headphones for my commute",
        "expected_product": "EL-AUD-91823",
        "agents_involved": ["DEMAND_SENSING", "INVENTORY_OPTIMIZER", "SUPPLIER_COLLABORATION", "LOGISTICS_OPTIMIZER"],
        "business_value": "Prevents stockouts, maintains 99.2% fill rate"
    },
    {
        "id": "SCENARIO-003",
        "name": "Cross-Division Basket Build",
        "description": "Customer building a project basket across multiple divisions",
        "customer_id": "CUST-00003",
        "query": "I'm renovating my home office and need a complete setup",
        "expected_product": "OT-CMP-67234",
        "agents_involved": ["CUSTOMER_INTELLIGENCE", "INVENTORY_OPTIMIZER", "FULFILLMENT_ORCHESTRATOR", "PRICING_AGENT"],
        "business_value": "Cross-sell increases basket size by 65%"
    }
]
