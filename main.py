from bs4 import BeautifulSoup
import csv  
import argparse

parser = argparse.ArgumentParser(description="Course name")
parser.add_argument('--course', type=str, required=True, help="Name of the course")
args = parser.parse_args()

course_dict = {
    "mth": ["HTML_Pages/MTH102AA_ Mathematics - II.html", "CSV_results/mth_res.csv"],
    "lif": ["HTML_Pages/LIF101AA_ Introduction To Biology.html", "CSV_results/lif_res.csv"],
    "chm": ["HTML_Pages/CHM102AA_ General Chemistry.html", "CSV_results/chm_res.csv"],
    "ta": ["HTML_Pages/TA101AA_ Engineering Graphics.html", "CSV_results/ta_res.csv"],
    "phy": ["HTML_Pages/PHY102AA_ Physics-I.html", "CSV_results/phy_res.csv"]
}

if args.course.lower in course_dict.keys():

    html_path = course_dict[args.course.lower][0]
    with open(html_path, 'r', encoding="utf8") as html_text:
        content = html_text.read()

        soup = BeautifulSoup(content, 'lxml')

        temp = soup.find_all('div', class_='weekDetailsBox')

        info = []
        for i in range(len(temp)):
            lectures = temp[i].find_all('div', class_='lectureInfoBoxText')
            lecture_link = temp[i].find_all('a')

            for j in range(len(lectures)):
                info.append([lectures[j].text.split('\n')[1][36:], lecture_link[j]['href'], i])

        # print(info)

        fields = ['Video Name', 'Link to the lecture', 'Week Number']
        n = int(input("Enter the value of n: (Latest n videos to be fetched) \n"))

        result_file = course_dict[args.course.lower][1]

        with open(result_file, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile) 
                
            csvwriter.writerow(fields) 
            if n > len(info):
                print("The entered of value of n is more than total number of videos uploaded")
                print("Scraped the data of all uploaded videos and written in the result file")
                csvwriter.writerows(info)
            else:
                print("Scraped the data of latest " + str(n) + " videos uploaded, and written in result file")
                csvwriter.writerows(info[-1 * n : ])
else:
    print("The script doesnt scrap for the given course yet!")

