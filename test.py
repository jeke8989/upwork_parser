from core import get_info_list
import asyncio
import config
import json
from keybods import create_btn



subs = {
    "status": "success",
    "response": {
        "stasus": 200,
        "jobs": [
            {
                "Created Date": 1726610370469,
                "Subscribe": "1726609240472x770120660674471300",
                "Created By": "admin_user_web-scraping-gdn_test",
                "Modified Date": 1726610370470,
                "client_job_info": "323",
                "client_job_rate": "32",
                "client_location": "323",
                "description": "323",
                "link": "323",
                "location_freelancer": "32",
                "posted_date": "323",
                "price": "32",
                "title": "323",
                "_id": "1726610370468x816143841096277400"
            }
        ],
        "sub_link": "https://www.upwork.com/nx/search/jobs/?q=bubble",
        "sub_id": "42452523",
        "subscription_status": "ACTIVE",
        "send_email": False
    }
}

link = 'https://www.upwork.com/nx/search/jobs/?q=bubble'
version = 'test'
host_url = f"https://web-scraping-gdn.bubbleapps.io/version-{version}/api/1.1/wf/get_jobs"
token_bubble = config.token_bubble
job = {
                "Created Date": 1726610370469,
                "Subscribe": "1726609240472x770120660674471300",
                "Created By": "admin_user_web-scraping-gdn_test",
                "Modified Date": 1726610370470,
                "client_job_info": "323",
                "client_job_rate": "32",
                "client_location": "323",
                "description": """I’m looking for a data scientist who is able to analyze international trade data in terms of quantity and value of exported and imported goods, to and from United States.  The data is downloaded from trade.gov website, in any format of your choosing.""",
                "link": "https://www.upwork.com/nx/search/jobs/?nbs=1",
                "location_freelancer": "32",
                "posted_date": "3 days ago",
                "price": "Fixed Price",
                "title": "International Trade Data Scientist",
                "_id": "1726610370468x816143841096277400"
            }



#Отправка Telegram уведомление
async def send_telegram(tg_chat_id: str, job: dict, subs: dict):
    url = job['link']
    keybord = await create_btn(url)
    text = f"""New JOB Upwork\n\n<b>{job["title"]}</b>\n\n<i>{job["price"]}</i>\n\n{job['description']}\n\n<i>Posted date: {job['posted_date']}</i>\n\n\n<b>Subscription ID: {subs['response']['sub_id']}</b>\nSubscription Link: {subs['response']['sub_link']}"""
    await config.bot.send_message(chat_id=tg_chat_id, text=text, reply_markup=keybord, parse_mode = "HTML")

async def main():
    data = await get_info_list(url="https://www.upwork.com/nx/search/jobs/?q=bubble")
    j_data = json.dumps(data, ensure_ascii=False, indent=4)
    print(j_data)

    
    
if __name__ == "__main__":
    asyncio.run(main())