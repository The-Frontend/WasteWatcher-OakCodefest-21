class Dish {
  Dish({
    this.name,
    this.ingredients,
    this.quantity,
  });

  String name;
  List<String> ingredients;
  double quantity;

  factory Dish.fromMap(Map<String, dynamic> json) => Dish(
        name: json["name"],
        ingredients: List<String>.from(json["ingredients"].map((x) => x)),
        quantity: json["quantity"].toDouble(),
      );

  Map<String, dynamic> toMap() => {
        "name": name,
        "ingredients": List<dynamic>.from(ingredients.map((x) => x)),
        "quantity": quantity,
      };
}
