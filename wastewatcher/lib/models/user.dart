class User {
  User({
    this.id,
    this.name,
    this.massWasted,
  });

  int id;
  String name;
  double massWasted;

  factory User.fromMap(Map<String, dynamic> json) => User(
        id: json["id"],
        name: json["name"],
        massWasted: json["mass_wasted"].toDouble(),
      );

  Map<String, dynamic> toMap() => {
        "id": id,
        "name": name,
        "mass_wasted": massWasted,
      };
}
