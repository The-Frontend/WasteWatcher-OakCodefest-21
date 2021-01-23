import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:wastewatcher/models/user.dart';

final userProvider = Provider.autoDispose<User>((ref) {
  ref.maintainState = true;
  // Defining a dummy user
  return User(
    id: 1,
    name: 'John Doe',
    massWasted: 5.3,
  );
});
