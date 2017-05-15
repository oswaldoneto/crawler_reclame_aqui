import json

with open('/Users/oswaldo/complain.json') as data:
    data = json.load(data)

problem_list = []
for complain in data:
    problem_list.append(complain['category'])


problem_list = set(problem_list)


with open('/Users/oswaldo/Dev/crawler_reclame_aqui/output/problem.txt','w') as output_file:
    for problem in problem_list:
        output_file.write('%s\n' % problem)

output_file.close()





