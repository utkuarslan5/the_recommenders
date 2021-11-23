#from subset.KNN import KNN
from subset.Users import Users

def main():

    print("Generating users . . .")

    num_users = 1
    num_PL_perUser = 10
    users = Users()
    users.generate_users(num_users,num_PL_perUser)

    print("Generating ratings . . . ")
    users.ratings()

    print("train KNN . . .")

    # knn = KNN()
    # knn.train()

if __name__ == "__main__":
   main()