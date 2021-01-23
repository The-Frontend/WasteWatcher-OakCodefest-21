import 'package:flutter_riverpod/all.dart';
import 'package:http/http.dart' as http;
import 'package:wastewatcher/models/dish.dart';
import 'package:wastewatcher/models/edamamApiResponse.dart';
import 'package:meta/meta.dart';
import 'dart:convert';

final apiServiceProvider = Provider<APIService>((ref) {
  return APIService();
});

class APIService {
  static const API_BASE_URL = 'https://wastewatcher-api.herokuapp.com';

  Future<EdamamApiResponse> searchEdamamDishes({@required String query}) async {
    final response = await http.get(
      '$API_BASE_URL/dish-search/?query=$query',
    );
    return EdamamApiResponse.fromMap(
      json.decode(
        response.body,
      ),
    );
  }

  Future<List<Dish>> getDishes({@required int userId}) async {
    final response = await http.get(
      '$API_BASE_URL/dishes/$userId',
    );
    final dishesJson = List<Map<String, dynamic>>.from(
      json.decode(response.body),
    );
    return dishesJson
        .map(
          (dishJson) => Dish.fromMap(dishJson),
        )
        .toList();
  }
}
