link_jon = "/jobs/Improve-tech-startup-span-class-highlight-Bubble-span-platform_~021836155531656867459/?referrer_url_path=/nx/search/jobs/"
job_link = str(link_jon).replace('jobs/', "").split("/?")[0]
url = f"https://www.upwork.com/freelance-jobs/apply{job_link}"


print(url)