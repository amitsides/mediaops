import openai
import os
import random

# Define the schema
schema = {
    "Vertical": ["Technology", "Finance", "Healthcare", "Education", "Retail", "Entertainment", "Travel", "Food"],
    "Sub-Vertical": {
        "Technology": ["Software", "Hardware", "Cloud Computing", "AI", "Cybersecurity", "Mobile Apps"],
        "Finance": ["Banking", "Investment", "Insurance", "FinTech", "Cryptocurrency"],
        "Healthcare": ["Hospitals", "Pharmaceuticals", "Medical Devices", "Telemedicine", "Mental Health"],
        "Education": ["K-12", "Higher Education", "Online Learning", "Vocational Training", "Corporate Training"],
        "Retail": ["E-commerce", "Brick-and-Mortar", "Fashion", "Electronics", "Groceries"],
        "Entertainment": ["Movies", "Music", "Gaming", "Streaming", "Live Events"],
        "Travel": ["Airlines", "Hotels", "Tourism", "Travel Agencies", "Car Rentals"],
        "Food": ["Restaurants", "Food Delivery", "Grocery Stores", "Food Manufacturing", "Agriculture"],
    },
    "Topic": {
        "Software": ["Cloud Migration", "DevOps", "Software Development", "Data Analytics", "UI/UX Design"],
        "Hardware": ["Chip Design", "Server Management", "IoT Devices", "Computer Peripherals", "Robotics"],
        "Cloud Computing": ["AWS", "Azure", "GCP", "Serverless", "Containerization"],
        "AI": ["Machine Learning", "Natural Language Processing", "Computer Vision", "Deep Learning", "Generative AI"],
        "Cybersecurity": ["Threat Detection", "Data Privacy", "Network Security", "Incident Response", "Vulnerability Management"],
        "Mobile Apps": ["iOS Development", "Android Development", "Cross-Platform Development", "Mobile Marketing", "App Security"],
        "Banking": ["Digital Banking", "Mobile Payments", "Fraud Detection", "Regulatory Compliance", "Wealth Management"],
        "Investment": ["Stock Trading", "Mutual Funds", "Real Estate", "Venture Capital", "Private Equity"],
        "Insurance": ["Life Insurance", "Health Insurance", "Property Insurance", "Auto Insurance", "Cyber Insurance"],
        "FinTech": ["Payment Gateways", "Lending Platforms", "Personal Finance Apps", "Blockchain", "RegTech"],
        "Cryptocurrency": ["Bitcoin", "Ethereum", "DeFi", "NFTs", "Blockchain Analysis"],
        "Hospitals": ["Patient Care", "Medical Research", "Hospital Management", "Emergency Services", "Medical Technology"],
        "Pharmaceuticals": ["Drug Discovery", "Clinical Trials", "Generic Drugs", "Biopharmaceuticals", "Regulatory Affairs"],
        "Medical Devices": ["Diagnostic Equipment", "Surgical Instruments", "Wearable Devices", "Prosthetics", "Medical Imaging"],
        "Telemedicine": ["Remote Patient Monitoring", "Virtual Consultations", "Telehealth Platforms", "Digital Therapeutics", "Online Prescriptions"],
        "Mental Health": ["Therapy Apps", "Mental Wellness Platforms", "Stress Management", "Anxiety Treatment", "Depression Support"],
        "K-12": ["Curriculum Development", "Classroom Technology", "Teacher Training", "Student Assessment", "Special Education"],
        "Higher Education": ["Online Degrees", "Student Retention", "Research Funding", "Campus Management", "Admissions"],
        "Online Learning": ["Learning Management Systems", "MOOCs", "Microlearning", "Personalized Learning", "Skills Training"],
        "Vocational Training": ["Trade Skills", "Technical Certifications", "Career Development", "Apprenticeships", "Job Placement"],
        "Corporate Training": ["Leadership Development", "Compliance Training", "Soft Skills", "Technical Skills", "Onboarding"],
        "E-commerce": ["Online Marketing", "Inventory Management", "Shipping and Logistics", "Customer Service", "Payment Processing"],
        "Brick-and-Mortar": ["Store Layout", "Point of Sale Systems", "Retail Staffing", "Customer Experience", "Local Marketing"],
        "Fashion": ["Apparel Design", "Supply Chain Management", "E-commerce Platforms", "Trend Forecasting", "Sustainable Fashion"],
        "Electronics": ["Consumer Electronics", "Component Sourcing", "Product Development", "Repair Services", "Recycling"],
        "Groceries": ["Supply Chain", "Fresh Produce", "Online Delivery", "Store Operations", "Food Safety"],
        "Movies": ["Film Production", "Distribution", "Streaming Services", "Special Effects", "Screenwriting"],
        "Music": ["Record Labels", "Streaming Platforms", "Live Performances", "Music Production", "Artist Management"],
        "Gaming": ["Game Development", "Esports", "Streaming Platforms", "Game Design", "Virtual Reality"],
        "Streaming": ["Content Creation", "Video on Demand", "Live Streaming", "Subscription Services", "Advertising"],
        "Live Events": ["Concerts", "Festivals", "Sporting Events", "Conferences", "Theater"],
        "Airlines": ["Flight Operations", "Customer Service", "Loyalty Programs", "Route Planning", "Aircraft Maintenance"],
        "Hotels": ["Hospitality Management", "Online Booking", "Customer Reviews", "Room Service", "Event Planning"],
        "Tourism": ["Destination Marketing", "Travel Packages", "Cultural Tours", "Adventure Travel", "Sustainable Tourism"],
        "Travel Agencies": ["Online Travel Agents", "Corporate Travel", "Group Travel", "Custom Itineraries", "Travel Insurance"],
        "Car Rentals": ["Fleet Management", "Online Reservations", "Customer Service", "Insurance", "Electric Vehicles"],
        "Restaurants": ["Menu Development", "Kitchen Management", "Customer Service", "Online Ordering", "Food Delivery"],
        "Food Delivery": ["Delivery Logistics", "Mobile Apps", "Restaurant Partnerships", "Customer Support", "Payment Processing"],
        "Grocery Stores": ["Inventory Management", "Online Ordering", "Delivery Services", "Customer Loyalty", "Fresh Produce"],
        "Food Manufacturing": ["Food Processing", "Packaging", "Quality Control", "Supply Chain", "Distribution"],
        "Agriculture": ["Crop Production", "Livestock Farming", "Sustainable Agriculture", "Farm Technology", "Supply Chain"],
    },
    "GEO": ["USA", "Canada", "UK", "Germany", "France", "Japan", "China", "India", "Brazil", "Australia"],
    "Platform": ["Web", "Mobile", "Desktop", "Social Media", "Cloud", "IoT"],
}

def generate_random_content():
    """Generates random content based on the schema."""

    vertical = random.choice(schema["Vertical"])
    sub_vertical = random.choice(schema["Sub-Vertical"][vertical])
    topic = random.choice(schema["Topic"][sub_vertical])
    geo = random.choice(schema["GEO"])
    platform = random.choice(schema["Platform"])

    return {
        "Vertical": vertical,
        "Sub-Vertical": sub_vertical,
        "Topic": topic,
        "GEO": geo,
        "Platform": platform,
    }

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or set it directly: openai.api_key = "YOUR_API_KEY"

def generate_values_openai(vertical=None, sub_vertical=None, topic=None, geo=None, platform=None):
    """Generates values using OpenAI based on provided context."""

    prompt = "Generate a data point with the following fields: Vertical, Sub-Vertical, Topic, GEO, Platform."

    if vertical:
        prompt += f" Vertical: {vertical}."
    if sub_vertical:
        prompt += f" Sub-Vertical: {sub_vertical}."
    if topic:
        prompt += f" Topic: {topic}."
    if geo:
        prompt += f" GEO: {geo}."
    if platform:
        prompt += f" Platform: {platform}."

    prompt += " Provide only the values, separated by commas, in the order: Vertical, Sub-Vertical, Topic, GEO, Platform."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or another suitable engine
            prompt=prompt,
            max_tokens=100,
            temperature=0.7,
            n=1,
            stop=None,
        )

        result = response.choices[0].text.strip()
        values = result.split(",")
        values = [v.strip() for v in values] #remove extra spaces.
        if len(values) == 5:
            return {
                "Vertical": values[0],
                "Sub-Vertical": values[1],
                "Topic": values[2],
                "GEO": values[3],
                "Platform": values[4],
            }
        else:
            return {"error": "OpenAI returned an incorrect number of values."}

    except Exception as e:
        return {"error": f"An error occurred: {e}"}

# Example usage:
result1 = generate_values_openai()
print(result1)

result2 = generate_values_openai(vertical="Technology")
print(result2)

result3 = generate_values_openai(topic="Machine Learning", geo="USA")
print(result3)

result4 = generate_values_openai(vertical="Finance", sub_vertical="Banking", topic="Digital Banking", geo="Canada", platform="Mobile")
print(result4)

result5 = generate_values_openai(vertical = "Food", sub_vertical= "Restaurants", topic = "Menu Development")
print(result5)