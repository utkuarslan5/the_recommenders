import pandas as pd


class Apriori:
    pass
    """ Frequency Sets """

    def __init__(self, path='export/songs.csv'):
        self.df_csv = pd.read_csv(path)
        count = self.df_csv['track_name'].value_counts()
        # Quite the mind, open the heart
        # print(count)
        # count = self.df_csv['pid']['artist_name'].value_counts()
        # print(count)

    def calculate_pair_support(self, feature_a, feature_b, column='Artist', **kwargs):
        self.df_csv.groupby(['pid'])
        a, b, anb = 0, 0, 0
        ppid, aa, bb, aanbb = [], [], [], []
        # 'Artist', 'Track', 'Album'
        if column == 'Artist':
            col = 4
        elif column == 'Track':
            col = 3
        elif column == 'Album':
            col = 5
        else:
            print("Enter a valid column {'Artist', 'Track', 'Album'}")
        temp = -1
        stats = []
        for i in range(len(self.df_csv)):
            pid = self.df_csv.iloc[i, 1]
            if pid != temp:
                if a != 0 or b != 0:
                    ppid.append(pid)
                    aa.append(a)
                    bb.append(b)
                    aanbb.append(anb)
                a, b, anb = 0, 0, 0
                temp = pid

            if self.df_csv.iloc[i, col] == feature_a:
                a += 1
            if self.df_csv.iloc[i, col] == feature_b:
                b += 1
            if a != 0 and b != 0:
                anb = min(a, b)

        support_df = pd.DataFrame([ppid, aa, bb, aanbb]).T
        support_df.columns = ['pid', column+': '+str(feature_a), column+': '+str(feature_b), str(feature_a)+' and '+str(feature_b)]
        pd.set_option('display.max_columns', 4)
        return support_df
        # self.['artist_name'] =
        # df_csv['support'] = rated_movies_df['rating'].apply(lambda x: 1 if x > 3 else 0)


if __name__ == '__main__':
    apriori = Apriori()
