"""
This module is used by the Lambda function which gives details about train disruptions.
"""

import csv


class CheckDisruptions:
    """
    A class to check for train disruptions from a CSV file which stores
    the all train disruptions in the Netherlands from 2024. This class reads
    disruption data from a specified CSV file, processes it, and provides
    methods to retrieve disruption information for a given station.
    """

    DISRUPTIONS_FILE_PATH = "./ns_trains_disruptions_2024.csv"

    @classmethod
    def get_disruptions(cls):
        """
        Retrieves and processes train disruption data from a CSV file. It parses
        each row and stores for each train station the first existent disruption.

        Returns
        -------
        dict
            A dictionary where keys are the starting station names and values
            are a list containing:
            - The destination station
            - The cause of the disruption
            - The duration of the disruption in minutes
            Returns an empty dictionary if the file is not found.
        """

        # load the data
        try:
            with open(cls.DISRUPTIONS_FILE_PATH, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                all_disruptions = list(reader)
        except FileNotFoundError:
            return {}

        # get the first existent disruption for each train station
        disruptions_from_station = {}
        seen_start_stations = set()

        for row in all_disruptions:
            line = row["ns_lines"]

            if line.count(" - ") == 1:
                start_station, destination_station = line.split(" - ")
            elif line.count("-") == 1:
                start_station, destination_station = line.split("-")
            else:
                # skip malformed lines
                continue

            # normalize spacing
            start_station = start_station.strip()
            destination_station = destination_station.strip()

            # add the start station only if it has not been seen
            if start_station not in seen_start_stations:
                seen_start_stations.add(start_station)
                disruptions_from_station[start_station] = [
                    destination_station,
                    row["statistical_cause_en"],
                    row["duration_minutes"],
                ]

        return disruptions_from_station

    @classmethod
    def get_disruption_from_station(cls, station_name):
        """
        Retrieves disruption information for a specified train station.

        Parameters
        ----------
        station_name : str
            The name of the train station to check for disruptions.

        Returns
        -------
        str
            A formatted string indicating the disruption status.
        """

        disruptions = cls.get_disruptions()
        all_stations = list(disruptions.keys()) + ["Enschede"]

        if station_name not in all_stations:
            return f"There is no train station in {station_name}."

        try:
            destination_station, cause, duration = disruptions[station_name]
            return (
                f"There is a disruption from {station_name} to {destination_station}"
                + f" of around {duration} minutes with the cause '{cause}'."
            )
        except KeyError:
            return f"You are lucky. There are no disruptions from {station_name}."


if __name__ == "__main__":
    print(CheckDisruptions.get_disruption_from_station("Enschede"))
