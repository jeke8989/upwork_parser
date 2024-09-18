from core import get_info_list
import asyncio
import config
import json
from keybods import create_btn
from core import event_job_subscription, post_bubble_job_add



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
token_bubble = config.token_bubble
api_key="1111"
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

host = "https://web-scraping-gdn.bubbleapps.io"
job = {
        "title": "Bubble.io Developer for Custom CRM",
        "description": "Project Description\nThe mobile application will leverage Bubble.io to educate people with no business background but having visionary ideas through step by step interactive training modules  featuring animated videos. Users will engage with these tasks by implementing them in their own environments and submitting their assignments through the app. The application will also integrate a backend system for customer relationship management (CRM) and database functionalities, ensuring efficient tracking of user progress and task completion.\n\nKey Features\n1.\tAnimated Training Modules: Users will view animated videos for each task, created using Bubble's design tools.\n2.\tTask Implementation: Users can implement tasks on their own and submit assignments via the app's user-friendly interface.\n3.\tExcel Template Management: Each task will include an Excel template that users can fill out and upload through the app.\n4.\tBackend CRM: A robust backend system built on Bubble to manage user data, track progress, and provide analytics.\n5.\tResponsive Design: The app will be optimized for mobile use, ensuring a seamless experience on various devices.\nRequirement Description\nFunctional Requirements\n1.\tUser Authentication:\n•\tImplement user registration and login functionalities using Bubble's built-in authentication features.\n•\tSupport for social media login options if desired.\n2.\tTask Management:\n•\tAbility to browse tasks, displayed in a mobile-friendly format.\n•\tIntegration of animated videos for each task using Bubble's video elements.\n3.\tAssignment Submission:\n•\tUsers can upload completed Excel templates directly through the app.\n•\tProvide submission confirmation and feedback mechanisms.\n4.\tProgress Tracking:\n•\tDashboard for users to view completed tasks and assignments, utilizing Bubble's data display capabilities.\n•\tVisual representation of progress through charts or graphs created within Bubble.\n5.\tNotifications:\n•\tPush notifications for new tasks, reminders for pending assignments, and updates using Bubble's notification features.\nNon-Functional Requirements\n1.\tPerformance:\n•\tThe app should load content quickly, ideally within 2 seconds, leveraging Bubble's optimization tools.\nSecurity:\n•\tEnsure user data is encrypted during transmission and storage using Bubble's security features.\n•\tCompliance with data protection regulations (e.g., GDPR).\nUsability:\n•\tThe interface must be intuitive, designed with responsive editing in Bubble to accommodate various screen sizes.\nCompatibility:\n•\tThe app should be compatible with both iOS and Android platforms through wrapping solutions like BDK or Natively if necessary.\nTechnical Requirements\nDevelopment Tools:\nUtilize Bubble.io as the primary development platform for building both web and mobile components of the app.\nMobile Wrapping Solutions:\nConsider using wrappers like BDK or Natively to convert the Bubble web app into a native mobile app for distribution on app stores if needed.\nAPIs:\nIntegrate necessary APIs for handling file uploads (Excel templates) securely within the Bubble environment.\nTesting:\nImplement a testing strategy that includes unit tests, integration tests, and user acceptance testing (UAT) within the Bubble framework.",
        "price": "Hourly",
        "link": "/jobs/span-class-highlight-Bubble-span-Developer-for-Custom-CRM_~021836324357197634798/?referrer_url_path=/nx/search/jobs/"
    }
#Отправка Telegram уведомление
async def send_telegram(tg_chat_id: str, job: dict, subs: dict):
    url = job['link']
    keybord = await create_btn(url)
    text = f"""New JOB Upwork\n\n<b>{job["title"]}</b>\n\n<i>{job["price"]}</i>\n\n{job['description']}\n\n<i>Posted date: {job['posted_date']}</i>\n\n\n<b>Subscription ID: {subs['response']['sub_id']}</b>\nSubscription Link: {subs['response']['sub_link']}"""
    await config.bot.send_message(chat_id=tg_chat_id, text=text, reply_markup=keybord, parse_mode = "HTML")
#


async def main():
    n = await event_job_subscription(link_subs=link, version="test", api_key="1111", host=host)
    print(n)
   

    
    
if __name__ == "__main__":
    asyncio.run(main())