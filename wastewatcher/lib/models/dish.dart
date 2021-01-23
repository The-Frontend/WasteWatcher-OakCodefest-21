class Dish {
  Dish({
    this.id,
    this.userId,
    this.deviceId,
    this.dishName,
    this.ingredients,
    this.quantity,
  });

  int id;
  int userId;
  int deviceId;
  String dishName;
  List<String> ingredients;
  double quantity;

  factory Dish.fromMap(Map<String, dynamic> json) => Dish(
        id: json["id"],
        userId: json["user_id"],
        deviceId: json["device_id"],
        dishName: json["dish_name"],
        ingredients: List<String>.from(json["ingredients"].map((x) => x)),
        quantity: json["quantity"],
      );

  Map<String, dynamic> toMap() => {
        "id": id,
        "user_id": userId,
        "device_id": deviceId,
        "dish_name": dishName,
        "ingredients": List<dynamic>.from(ingredients.map((x) => x)),
        "quantity": quantity,
      };
}
