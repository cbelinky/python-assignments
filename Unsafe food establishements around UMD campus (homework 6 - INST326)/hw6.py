import pandas as pd
import sys

class FoodInspections():
    def __init__(self, path1, path2):
        """reads the two CSV files into dataframes and merges the two dataframes
        on the "Establishment_id" column using a left join with the inspection
        data as the left dataframe. Then stores the resulting merged dataframe
        in an attribute called inspections.

        Arguments:
            path1 {str} -- a string representing the file path to a csv.
            path2 {str} -- a string representing the file path to a csv.
        """
        df1 = pd.read_csv(path1)
        df2 = pd.read_csv(path2)
        df3 = pd.merge(df1, df2, how="left", on = "Establishment_id")
        self.inspections = df3

    def analyze(self, dist):
        """ calls the mask() method to get a dataframe with only the rows that
        meet the specified criteria. Finds out the maximum number of rows for a
        given Establishment ID in the masked dataframe and the maximum number of
        rows. Get the unique names that correspond to those Establishment IDs
        and returns a tuple consisting of the unique names, as a list, and the
        number of violations that those establishments were given.


        Arguments:
            dist {float} -- distance in miles from McKeldin Library

        Returns:
            Tuple -- a tuple consisting of the unique names, as a list, and the
        number of violations that those establishments were given.

        """
        masked = self.mask(dist)
        id_counts = masked.groupby('Establishment_id')['Establishment_id'].\
        count()
        max = id_counts.max()
        most_violations_num = id_counts[id_counts == max]
        most_violations = masked[masked['Establishment_id'].isin\
            (most_violations_num.index)]
        lst = most_violations["Name"].unique()
        return (lst, max)

    def mask(self, dist):
        """Applies a mask to the inspections dataframe filtering the data in
        the following ways: establishments that are within the distance
        specified in the 'dist' argument, the value of the "Inspection_type"
        is either "Monitoring" or "Comprehensive", and the value of the
        "Inspection_results" column is "Critical Violations observed".
        The method then returns the masked dataframe.

        Arguments:
            dist {float} -- distance in miles from McKeldin Library

        Returns:
            dataframe -- a masked dataframe filtered using the specification
            listed in the description above.
        """
        within_dist = self.inspections[(self.inspections['Distance_to_McKeldin'\
                                                         ] <= float(dist))]
        insp_type = within_dist[within_dist["Inspection_type"].isin(\
            ["Monitoring", "Comprehensive"])]
        masked_df = insp_type[(insp_type["Inspection_results"] ==\
                                 "Critical Violations observed")]
        return masked_df

def main(path_to_inspection, path_to_establishments, dist):
    """main function that instantiates a FoodInspection object and runs methods
    on the dataframe.

    Arguments:
        path_to_inspection {str} -- file path to inspection csv
        path_to_establishments {str} -- file path to establishments csv
        dist {float} -- distance in miles from McKeldin Library
    """
    my_inspections = FoodInspections(path_to_inspection, path_to_establishments)
    violations = my_inspections.analyze(dist)
    print("The establishments with the most violations were: " + \
        str(violations[0]) + " with " + str(violations[1]) + " violations.")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
