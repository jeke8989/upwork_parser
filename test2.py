import json
import logging
new_data = [
  {
    "title": "PowerQuery Data Retrieval from Public API",
    "description": "Deliverable: PowerQuery script that first ingests an excel table with input fields and then uses those inputs to construct an API query and return the queried data to an excel table in the specified format.  If query results exceed 1000 records, the query will need to paginate the results and then aggregated into a single table.  If the total results exceed 26,000 records, the query should return an error message that some results may not be returned (the openFDA API will only paginate to 26,000 records)\n\u2022\tDatabase: openFDA (https://open.fda.gov/) \no\tNo credentials required, it\u2019s a public API\n\u2022\tAPI: openFDA API (https://open.fda.gov/apis/) \n\u2022\tEndpoints: Device API Endpoints / Adverse Events\n\nINPUT TABLE FIELDS: The PowerQuery script should first ingest a table with these fields.  The API query should then be constructed using any of the fields which are not blank.  It is not required that all fields contain values, they should each be considered optional.\n\u2022\tProduct Problem\n\u2022\tPriduct Class\n\u2022\tEvent Type\n\u2022\tModel Number\n\u2022\tBand Name\n\u2022\tExemption Number\n\u2022\tManufacturer\n\u2022\tReport Number\n\u2022\tProduct Code\n\u2022\tUDI-Device Identifier\n\u2022\tPMA/510K Number\n\u2022\tDate Report Received by FDA (START)\n\u2022\tDate Report Received by FDA (END)\n\nDATA RETURN TABLE: The results of the query should be aggregated into a single table with the following columns:\n\u2022\tManufacturer \n\u2022\tBrand Name\n\u2022\tProduct Code\n\u2022\tCatalog Number\n\u2022\tType of Device\n\u2022\tDevice Problem\n\u2022\tMDR Report Key\n\u2022\tMDR Text Key\n\u2022\tReport Number\n\u2022\tDevice Sequence Number\n\u2022\tProduct Code\n\u2022\tUDI-Device Identifier\n\u2022\tUDI-Public\n\u2022\tCombination Product (y/n)\n\u2022\tReporter Country Code\n\u2022\tPMA/PMN Number\n\u2022\tNumber of Events Reported\n\u2022\tSummary Report (Y/N)\n\u2022\tReport Source\n\u2022\tSource Type\n\u2022\tReporter Occupation\n\u2022\tType of Report\n\u2022\tReport Date\n\u2022\tDate FDA Received\n\u2022\tIs this an Adverse Event Report?\n\u2022\tIs this a Product Problem Report?\n\u2022\tDevice Operator\n\u2022\tDevice Catalogue Number\n\u2022\tWas Device Available for Evaluation?\n\u2022\tIs the Reporter a Health Professional?\n\u2022\tDate Manufacturer Received\n\u2022\tDate Device Manufactured\n\u2022\tIs the Device Single Use?\n\u2022\tIs This a Reprocessed and Reused Single-Use Device?\n\u2022\tType of Device Usage\n\u2022\tPatient Sequence Number\n\u2022\tPatient Outcome(s)\n\u2022\tPatient Age\n\u2022\tPatient Sex\n",
    "price": "Fixed price",
    "link": "/jobs/PowerQuery-Data-Retrieval-from-Public-API_~021837886263275126660/?referrer_url_path=/nx/search/jobs/"
  },
  {
    "title": "Build a clone of AI Video Platform Sora or Kling  (Using open source framework MORA)",
    "description": "Budget: $2,000\n\nI am looking for an experienced developer to create a prototype text-to-video platform using the open-source Mora framework, similar to the functionality of Sora and Kling. Basically make a clone of Sora and Kling using open source Mora framework. Copy the same UI and functionality as that of Kling.\n\nKling for reference: https://klingai.com/\n\nThe project will involve building a web-based tool that allows users to generate videos from text prompts. The site should be simple, functional, and demonstrate the core capabilities of text-to-video generation using the Mora model. \n\nProject Scope:\n\n-Integrate the open source Mora multi-agent video generation framework.\n-Develop a user-friendly interface where users can input text prompts and generate videos.\n-Implement basic video output functionality, including downloading the generated videos.\n-Optimize the website for performance, ensuring it runs efficiently during video generation.\n-Ensure the site can handle different video generation scenarios (e.g., text-to-video, image-to-video).\n-Provide documentation and clean code for future scalability.\n\nDeliverables:\nA fully functional prototype website.\nDocumentation on how to deploy and manage the system.\nCodebase in a GitHub repository or similar version control system.\n\nTimeline: 4-6 weeks\n\nTo Apply:\nPlease share examples of your previous work, especially projects where you've worked on AI or video generation. Mention how you would approach integrating Mora into a live web environment.\n\nI look forward to working with a talented developer on this project!\n\nStart your application with the word \"LEMON\" so I know you've read everything properly. Thanks for your time!\n\n",
    "price": "Fixed price",
    "link": "/jobs/Build-clone-Video-Platform-Sora-Kling-Using-open-source-framework-MORA_~021837876409835739423/?referrer_url_path=/nx/search/jobs/"
  },
  {
    "title": "Enhance Mobile App Engagement with Advanced Data Analysis and Export Features",
    "description": "Job Description:\nWe are seeking a skilled and innovative developer to enhance the user engagement features of our\nmobile application. This project will involve the implementation of a robust system for liking and\ncommenting on news articles, as well as developing advanced data exporting capabilities. The goal\nis to ensure that the data generated from these interactions is clean, well-structured, and ready for\nin-depth analysis.\nJob Tags:\n\u2022 Mobile App Development\n\u2022 Backend Development\n\u2022 Data Analysis\n\u2022 Data Cleansing\n\u2022 Data Exporting\n\u2022 API Integration\n\u2022 Data Standardization",
    "price": "Fixed price",
    "link": "/jobs/Enhance-Mobile-App-Engagement-with-Advanced-Data-Analysis-and-Export-Features_~021837875463776993156/?referrer_url_path=/nx/search/jobs/"
  },
  {
    "title": "Goland Developer Needed for Innovative Project",
    "description": "We are seeking a skilled Golang developer to join our team for an exciting project. The ideal candidate will have experience in building scalable applications and API development using Golang. You will be responsible for writing clean, maintainable code and collaborating with our team to deliver high-quality software. If you are passionate about Golang and enjoy tackling complex problems, we would love to hear from you!",
    "price": "Fixed price",
    "link": "/jobs/Goland-Developer-Needed-for-Innovative-Project_~021837874533065348014/?referrer_url_path=/nx/search/jobs/"
  },
  {
    "title": "Web Application for video editing - FASTAPI/React",
    "description": "The scope is to optimize an FastApi back end (Python fule), Add simple React Front End  and deploy the  app the cloud server (Azure, GCP, AWS).\nNeed Excellent  experience with Python, FASTAPI, REACT, deployment.",
    "price": "Fixed price",
    "link": "/jobs/Web-Application-for-video-editing-FASTAPI-React_~021837872538376000430/?referrer_url_path=/nx/search/jobs/"
  },
  {
    "title": "AI driven Quality control system",
    "description": "We're looking for an experienced AI/ML developer with 5+ years experience who has experience in developing AI driven quality control system. \n\nThe system should have the following features:\n\n- Real time integration with XR (Extended Reality)\n- Real time product segmentation\n- Product tracking upon movement\n- Display dimensions on the product\n- Real time QA feedback\n\nI will share the high level requirement. The freelancer should come up with a detailed plan and cost.\n",
    "price": "Fixed price",
    "link": "/jobs/driven-Quality-control-system_~021837864004827552592/?referrer_url_path=/nx/search/jobs/"
  },
  {
    "title": "Python Developer Needed for Innovative Project",
    "description": "We are seeking a talented Python Developer to join our team for an exciting project. The ideal candidate will have experience in developing scalable web applications and a strong understanding of Python frameworks. Your responsibilities will include writing clean, maintainable code, collaborating with team members, and troubleshooting any issues that arise. If you are passionate about coding and looking for a challenging role, we would love to hear from you!",
    "price": "Fixed price",
    "link": "/jobs/span-class-highlight-Python-span-Developer-Needed-for-Innovative-Project_~021837858514032417055/?referrer_url_path=/nx/search/jobs/"
  },
  {
    "title": "AI SAAS defi Automated Crypto Scam Detection Crypto (memecoin) ",
    "description": "Magicvest is a SaaS platform that analyzes new cryptocurrencies on Dextool and Dexcreener, and sends signals for those with high scores (these cryptos are likely not scams). The analysis evaluates a promising crypto based on its tokenization, associated wallets (for example, if no single person holds multiple wallets in that crypto or if no one holds a large percentage of the total supply), the number of holders, the hype on social networks (like Twitter), and liquidity. All these factors together give the crypto a score.\n\n1. **Homepage:**\n   - **Subscription Access:** Users need to subscribe to access detailed information on meme coins.\n   - **Magic Signals:** Display the total number of signals sent by the AI regarding meme coins.\n\n2. **Wishlist/Watchlist Page:**\n   - **Watchlist:** Allow users to save and track meme coins they are interested in.\n\n3. **Best Investment Signals:**\n   - **Successful Signals:** Display the best investment signals with successful multipliers and the number of successful investments.\n\n4. **Detailed Crypto Analysis:**\n   - **Subscriber Data:** Number of subscribers for each coin.\n   - **Contract Information:** Contract link and details.\n   - **Top Holders:** Information on major holders.\n   - **Graphs:** Small graphs showing crypto trends.\n   - **Market Data:** Live market cap, sales, and purchase percentages.\n   - **Social Media Sentiment:** What people are saying about the project on platforms like Twitter.\n   - **Tokenomics:** Details on the tokenomics and number of tokens in circulation.\n   - **Additional Data:** Anything else deemed relevant by the AI.\n\n5. **Scam Detection:**\n   - **Scam Potential:** Number of cryptos flagged with high scam potential detected by the AI or user analyses.\n\n6. **Customer Support:**\n   - **Support Contact:** Page for customers to contact support.\n\n7. **New Crypto Launches:**\n   - **New Launches:** Information on new crypto launches and removal of outdated listings.\n\n8. **Presales:**\n   - **Presale Information:** Display cryptos in presale with options to view more details.\n\n9. **Chains:**\n   - **Chain-specific Cryptos:** Display cryptos categorized by their blockchain networks.\n\n10. **Search Functionality:**\n    - **Search Bar:** Allow users to search for specific cryptos or paste links for analysis.\n\n11. **Daily Gainers:**\n    - **Top Daily Gains:** Display cryptos with the highest gains in a day.\n\n12. **Strong Buy Recommendations:**\n    - **Investment Opportunities:** Cryptos recommended for immediate investment to take advantage of price increases.\n\n13. **Buy the Dips:**\n    - **Dip Opportunities:** Display cryptos that are reliable and have fallen in price since launch.\n\n14. **Safe Cryptos:**\n    - **Trusted Projects:** List of well-analyzed and trusted projects like Bitcoin, Ethereum, Solana, etc.\n\n15. **AI Magic Signals:**\n    - **New Investment Signals:** Daily updated list of new cryptos that are good investment opportunities according to the AI.\n\n16. **Interactive Content:**\n    - **Media:** Include clickable videos and photos for better user engagement ",
    "price": "Fixed price",
    "link": "/jobs/SAAS-defi-Automated-Crypto-Scam-Detection-Crypto-memecoin_~021837851372020551019/?referrer_url_path=/nx/search/jobs/"
  },
  {
    "title": "Code design",
    "description": "We are developing an innovative \"scouting\" platform that aims to identify and analyze talent or assets through advanced data processing and AI techniques. We are in the early stages and looking for a skilled developer to help us build a Proof of Concept (PoC) for our product.\n\nPlease initially link to examples of work, before we pass you the link to the design we have created.\n\nJob Description:\nWe are seeking a freelance developer to create the first version of our scouting product. This will be a Proof of Concept (PoC) development project. If you can provide examples of your prior work, we will share our initial design prototype and discuss project scope in further detail.\n\nResponsibilities:\n\nCollaborate with our team to understand the requirements and vision for the scouting product.\nDevelop a basic, functional version of the platform to demonstrate the core features.\nImplement data ingestion, processing, and visualization features using AI techniques as required.\nFocus on scalability and modularity to support future iterations and full-scale development.\nProvide technical documentation for the PoC version.\n\nQualifications:\n\nProven experience in developing PoCs or MVPs, especially in AI-driven products or data-heavy applications.\nStrong proficiency in relevant programming languages and frameworks (e.g., Python, JavaScript, React, Node.js, etc.).\nExperience with AI/ML libraries (e.g., TensorFlow, PyTorch, etc.) and familiarity with integrating AI models into products.\nKnowledge of databases (SQL, NoSQL) and cloud services (AWS, Google Cloud, Azure).\nStrong problem-solving skills and ability to work independently.",
    "price": "Fixed price",
    "link": "/jobs/Code-design_~021837837349803355487/?referrer_url_path=/nx/search/jobs/"
  },
  {
    "title": "AI developer for AI Agent Development (LangChain/LangGraph)",
    "description": "We are looking for a part-time freelance AI/Python developer experienced in AI development to work on a single project.\nThe goal is to build AI agent using LangChain and LangGraph to automate chat with clients, enabling function calling for external functionalities.\n\nResponsibilities:\n\n- Develop AI agents using LangChain/LangGraph\n- Design and implement AI models\n- Integrate AI agents into current systems\n\nRequirements:\n\n- Proficiency in Python\n- Experience with AI technologies (machine learning, NLP)\n- Strong problem-solving skills\n- Ability to work independently\n- Nice to have: Experience in designing custom AI solutions\n\nIf you're skilled in AI development and related frameworks (LangChain), we\u2019d love to hear from you",
    "price": "Fixed price",
    "link": "/jobs/developer-for-Agent-Development-LangChain-LangGraph_~021837818325996498271/?referrer_url_path=/nx/search/jobs/"
  }
]

subs = {
  "status": "success",
  "response": {
    "stasus": 200,
    "jobs": [
      "/jobs/Talent-Sourcing-Job-Posting-Expert_~021837498459101691780/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Youtube-Video-Editing-100-300-per-month-MUST-READ-DESCRIPTION_~021837498420029889360/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Digital-Comics-Tutor-for-Year-Old_~021837498269300160799/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Quarterly-SEO-Specialist-for-Website-Optimization_~021837498236633967967/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Voiceover-Artist-Needed-for-YouTube-Channel_~021837498209532215172/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Google-GMB-Review-Removal-Specialist-Needed_~021837498204950940385/?referrer_url_path=/nx/search/jobs/",
      "/jobs/looking-for-one-more-freelancers-specialized-scrapping-and-automation_~021837505648839414702/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Senior-Systems-Engineer_~021837502697205922079/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Combine-images-one-pdf-and-save-them-AWS_~021837501390579354337/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Expert-Needed-for-Automating-exe-Execution-and-Port-Whitelisting-for-Oracle_~021837499807150997380/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Engineer-Needed-for-Audio-Data-Processing-Flow_~021837499081632799007/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Prompt-Engineer-OpenAI-API-Few-Shot-Prompting_~021837498168476506960/?referrer_url_path=/nx/search/jobs/",
      "/jobs/span-class-highlight-Python-span-amp-Machine-Learning-Tutor-for-Labs-Assignment_~021837496212508973904/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Bet365-API_~021837496042368817439/?referrer_url_path=/nx/search/jobs/",
      "/jobs/need-PhD-200-related-computer-science-good-pay_~021837495365104376656/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Marketplace-Development-Strategy-Analysis-for-ClassBento_~021837494918394223440/?referrer_url_path=/nx/search/jobs/",
      "/jobs/span-class-highlight-Python-span-Developer-for-React-Site-Parsing_~021837508515371490128/?referrer_url_path=/nx/search/jobs/",
      "/jobs/GHL-Expert-Needed-for-Bot-Workflow-Development_~021837507741704542495/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Telegram-bot-developer-needed_~021837507631344091012/?referrer_url_path=/nx/search/jobs/",
      "/jobs/GenAI-POC-Development-and-Training-Assistance_~021837507112496103300/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Visual-Enhancement-for-Golf-Shot-Analysis_~021837506563720870175/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Need-API-Developer-Confirm-Data-Points-Available-thru-the-Practice-Panther-API_~021837505628809973099/?referrer_url_path=/nx/search/jobs/",
      "/jobs/software-for-admin-automation_~021837489411245496607/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Back-End-developer-with-AWS-NEO4J_~021837485946268123012/?referrer_url_path=/nx/search/jobs/",
      "/jobs/and-Engineer_~021837468510005547950/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Computer-Programming-Image-Processing-Expert-for-Virtual-Car-Showroom-background-replacer-blending_~021837459135122426593/?referrer_url_path=/nx/search/jobs/",
      "/jobs/SAAS-defi-Automated-Crypto-Scam-Detection-Crypto-memecoin_~021837447220110629712/?referrer_url_path=/nx/search/jobs/",
      "/jobs/AWS-Solutions-Architect_~021837440053030755152/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Fullstack-developer-for-startup-project_~021837438657712082283/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Consultant-for-Building-Plan-Processing-Website-Development_~021837437439033311108/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Full-Stack-Developer-Needed-for-Exciting-Project_~021837436296672891822/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Build-custom-Google-Cloud-image-based-Linux_~021837597597500504943/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Entwicklung-eines-News-Aggregator-Programms_~021837605567158602465/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Custom-Development-for-Insurance-Plan-Queries_~021837629335620098896/?referrer_url_path=/nx/search/jobs/",
      "/jobs/SAAS-defi-Automated-Crypto-Scam-Detection-Crypto-memecoin_~021837678097286560031/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Senior-span-class-highlight-Python-span-Consultant-Needed-for-Month-Project_~021837691333880085901/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Flask-Backend-Application-Setup-Quick-Job_~021837696412501216642/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Build-Automated-Content-Engine_~021837698380126034768/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Need-deploy-span-class-highlight-python-span-application-cloud_~021837704260348070625/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Automate-sending-bulk-certificates_~021837713796395244368/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Autofill-website-form_~021837772709819915088/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Flask-Backend-Application-Setup-Quick-Job_~021837812131764443984/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Development-Construction-Management-ERP-Software-with-Asset-Tracking_~021837814979839487327/?referrer_url_path=/nx/search/jobs/",
      "/jobs/developer-for-Agent-Development-LangChain-LangGraph_~021837818325996498271/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Code-design_~021837837349803355487/?referrer_url_path=/nx/search/jobs/",
      "/jobs/span-class-highlight-Python-span-Developer-Needed-for-Innovative-Project_~021837858514032417055/?referrer_url_path=/nx/search/jobs/",
      "/jobs/SAAS-defi-Automated-Crypto-Scam-Detection-Crypto-memecoin_~021837851372020551019/?referrer_url_path=/nx/search/jobs/",
      "/jobs/driven-Quality-control-system_~021837864004827552592/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Web-Application-for-video-editing-FASTAPI-React_~021837872538376000430/?referrer_url_path=/nx/search/jobs/",
      "/jobs/Goland-Developer-Needed-for-Innovative-Project_~021837874533065348014/?referrer_url_path=/nx/search/jobs/"
    ],
    "subscription_status": "ACTIVE",
    "email": "empty",
    "tg_bot_id": "173385085",
    "sub_link": "https://www.upwork.com/nx/search/jobs/?amount=500-999,1000-4999,5000-&contractor_tier=2,3&nbs=1&q=python&sort=recency&t=1",
    "sub_id": "6",
    "endpoint": "empty",
    "name": "Python"
  }
}




# Получаем список ссылок из subs
existing_jobs = subs["response"]["jobs"]

# Находим работы, которых нет в existing_jobs
not_found_jobs = [job for job in new_data if job["link"] not in existing_jobs]

# Выводим результаты
for i, job in enumerate(not_found_jobs):
    print(f"Index: {i}, Title: {job['title']}, Link: {job['link']}")