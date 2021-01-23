import 'package:flutter_riverpod/all.dart';
import 'package:wastewatcher/models/edamamApiResponse.dart';
import 'package:wastewatcher/services/apiService.dart';

final edamamApiResponseFutureProvider =
    FutureProvider.family<EdamamApiResponse, String>(
  (ProviderReference ref, String query) async {
    final apiService = ref.read(apiServiceProvider);
    final edamamApiResponse = await apiService.searchEdamamDishes(
      query: query,
    );
    return edamamApiResponse;
  },
);
