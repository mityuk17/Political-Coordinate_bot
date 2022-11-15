point_list = [
    [[-1,-1],[-2,-2],[2,-1],[2,1],[-2,2]],
    [[-2,0],[2,0],[1,-1],[0,0],[0,-1]],
[[-1,-1],[1,-1],[-1,1],[1,1],[0,-1]],
[[0,1],[1,-1],[0,1],[-1,-1],[0,-2]],
[[1,1],[-1,0],[1,-1],[0,-1],[-2,0]],
[[1,0],[1,-1],[-1,1],[2,-1],[-1,-1]],
[[0,0],[-1,-1],[1,1],[0,-1],[-1,-2]],
[[0,1],[-2,2],[0,-1],[1,-2],[-1,-1]],
[[-2,0],[0,1],[1,0],[1,-1],[-1,1]],
[[-2,2],[1,1],[-1,0],[0,1],[1,-1],[1,2],[0,0],[-1,-2],[0,-2]],
[[1,0],[-1,0],[0,2],[0,1]],
[[1,-1],[1,1],[-1,-1],[-1,1]],
[[0,-1],[0,1],[0,2]],
[[2,2],[1,1],[-1,0],[-1,-1]],
[[0,-1],[-1,0],[0,1],[1,-1],[1,1]],
[[1,-1],[-1,0],[0,0],[1,1],[2,-1],[0,2]],
[[0,2],[1,0],[1,1],[1,-1],[-2,-2]],
[[0,2],[1,1],[-1,-1],[1,-1],[0,-2]],
[[-2,0],[0,-1],[1,2]]

]
def get_question(number):
    variants= []
    with open('questions.txt') as f:
        file = f.readlines()
        for i in range(len(file)):
            if file[i].startswith(f'{str(number+1)}.'):
                question = file[i]
                for j in range(1,15):
                    if file[i+j].startswith(f'{str(j)})'):
                        variants.append(file[i+j])
                    else:
                        break
                break
    ans = [question,[]]
    for i in range(len(variants)):
        ans[1].append([variants[i],point_list[number][i]])
    return ans


