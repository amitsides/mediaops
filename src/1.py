from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.ad import Ad
import hashlib
import requests
from io import BytesIO
from PIL import Image

# Initialize the Facebook Ads API
access_token = 'YOUR_ACCESS_TOKEN'
app_id = 'YOUR_APP_ID'
app_secret = 'YOUR_APP_SECRET'
FacebookAdsApi.init(access_token=access_token)

# Function to get image hash
def get_image_hash(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return hashlib.md5(img.tobytes()).hexdigest()

# Function to get best performing creatives
def get_best_creatives(account_id):
    account = AdAccount(account_id)
    
    # Get ads with insights
    ads = account.get_ads(fields=[
        'id', 'creative', 'insights.date_preset(last_30d){impressions,clicks,spend}'
    ])
    
    creatives = []
    image_hashes = set()
    
    for ad in ads:
        if 'insights' in ad:
            insights = ad['insights']['data'][0]
            creative = AdCreative(ad['creative']['id'])
            creative_data = creative.api_get(fields=[
                'id', 'name', 'image_url', 'object_story_spec'
            ])
            
            if 'image_url' in creative_data:
                image_hash = get_image_hash(creative_data['image_url'])
                
                if image_hash not in image_hashes:
                    image_hashes.add(image_hash)
                    creatives.append({
                        'id': creative_data['id'],
                        'name': creative_data.get('name', ''),
                        'image_url': creative_data['image_url'],
                        'impressions': insights['impressions'],
                        'clicks': insights['clicks'],
                        'spend': insights['spend'],
                        'ctr': float(insights['clicks']) / float(insights['impressions']) if float(insights['impressions']) > 0 else 0,
                        'image_hash': image_hash
                    })
    
    # Sort creatives by CTR
    creatives.sort(key=lambda x: x['ctr'], reverse=True)
    return creatives

# List of account IDs
account_ids = ['ACCOUNT_ID_1', 'ACCOUNT_ID_2', 'ACCOUNT_ID_3']

all_creatives = []

for account_id in account_ids:
    all_creatives.extend(get_best_creatives(account_id))

# Sort all creatives by CTR
all_creatives.sort(key=lambda x: x['ctr'], reverse=True)

# Print top 10 creatives
for creative in all_creatives[:10]:
    print(f"Creative ID: {creative['id']}")
    print(f"Name: {creative['name']}")
    print(f"Image URL: {creative['image_url']}")
    print(f"CTR: {creative['ctr']:.2%}")
    print(f"Impressions: {creative['impressions']}")
    print(f"Clicks: {creative['clicks']}")
    print(f"Spend: ${creative['spend']}")
    print("---")
