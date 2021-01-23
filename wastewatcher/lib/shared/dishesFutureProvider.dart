import 'package:flutter_riverpod/all.dart';
import 'package:wastewatcher/models/dish.dart';
import 'package:wastewatcher/services/apiService.dart';
import 'package:wastewatcher/shared/userProvider.dart';

final dishesFutureProvider = FutureProvider.autoDispose<List<Dish>>(
  (ref) async {
    ref.maintainState = true;
    final apiService = ref.read(apiServiceProvider);
    final user = ref.read(userProvider);
    final dishes = await apiService.getDishes(
      userId: user.id,
    );
    return dishes;
  },
);
