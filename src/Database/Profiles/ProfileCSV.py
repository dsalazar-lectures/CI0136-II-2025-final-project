import csv
import os


class ProfileCSV:
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["user_id", "favorite_foods", "unfavorite_foods", "favorite_menus"]
                )

    def create_profile(self, profile_data):

        new_profile = {
            "user_id": str(profile_data["user_id"]),
            "favorite_foods": ";".join(profile_data["favorite_foods"]),
            "unfavorite_foods": ";".join(profile_data["unfavorite_foods"]),
            "favorite_menus": ";".join(profile_data["favorite_menus"]),
        }

        # Appends new profile to CSV file
        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "user_id",
                    "favorite_foods",
                    "unfavorite_foods",
                    "favorite_menus",
                ],
            )
            writer.writerow(new_profile)

        return new_profile

    def get_profile(self, user_id: int):
        if not os.path.exists(self.file_path):
            return None
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for csv_row in reader:
                # user_id in CSV is string
                if csv_row.get("user_id") == str(user_id):
                    return {
                        "user_id": int(csv_row.get("user_id", 0)),
                        "favorite_foods": csv_row.get("favorite_foods", ""),
                        "unfavorite_foods": csv_row.get("unfavorite_foods", ""),
                        "favorite_menus": csv_row.get("favorite_menus", ""),
                    }
        return None

    def update_fields(self, user_id: int, fields: dict):
        if not os.path.exists(self.file_path):
            return None

        fieldnames = ["user_id", "favorite_foods", "unfavorite_foods", "favorite_menus"]
        rows = []
        found = False

        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for csv_row in reader:
                if csv_row.get("user_id") == str(user_id):
                    found = True
                    merged = dict(csv_row)
                    for field_name, field_value in fields.items():
                        if field_name not in fieldnames or field_name == "user_id":
                            continue
                        if isinstance(field_value, list):
                            merged[field_name] = (
                                ";".join(field_value) if field_value else ""
                            )
                        else:
                            merged[field_name] = (
                                field_value if field_value is not None else ""
                            )
                    rows.append(merged)
                else:
                    rows.append(csv_row)

        if not found:
            return None

        # Rewrite the entire file
        with open(self.file_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row_dict in rows:
                # Ensure all columns exist
                output_row = {k: row_dict.get(k, "") for k in fieldnames}
                writer.writerow(output_row)

        # Return the updated row
        return self.get_profile(user_id)

    def get_profile_by_user_id(self, user_id: int):
        """Get a profile by user_id"""
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["user_id"] == str(user_id):
                    return {
                        "user_id": row["user_id"],
                        "favorite_foods": (
                            row["favorite_foods"].split(";")
                            if row["favorite_foods"]
                            else []
                        ),
                        "unfavorite_foods": (
                            row["unfavorite_foods"].split(";")
                            if row["unfavorite_foods"]
                            else []
                        ),
                        "favorite_menus": (
                            row["favorite_menus"].split(";")
                            if row["favorite_menus"]
                            else []
                        ),
                    }
        return None

    def update_profile(self, user_id: int, profile_data: dict):
        """Update a profile by user_id"""
        rows = []
        updated = False

        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["user_id"] == str(user_id):
                    # Update the row with new data
                    row["favorite_foods"] = ";".join(
                        profile_data.get("favorite_foods", [])
                    )
                    row["unfavorite_foods"] = ";".join(
                        profile_data.get("unfavorite_foods", [])
                    )
                    row["favorite_menus"] = ";".join(
                        profile_data.get("favorite_menus", [])
                    )
                    updated = True
                rows.append(row)

        if updated:
            with open(self.file_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        return updated
