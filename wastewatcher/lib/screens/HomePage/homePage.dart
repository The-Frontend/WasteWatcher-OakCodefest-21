import 'package:flutter/material.dart';
import 'package:flutter_riverpod/all.dart';

final counterStateProvider = StateProvider.autoDispose<int>((ref) {
  return 0;
});

class HomePage extends ConsumerWidget {
  void _incrementCounter(BuildContext context) {
    context.read(counterStateProvider).state += 1;
  }

  @override
  Widget build(BuildContext context, ScopedReader watch) {
    final counterState = watch(counterStateProvider);
    return Scaffold(
      body: Center(
        child: Text(
          counterState.state.toString(),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _incrementCounter(context),
      ),
    );
  }
}
