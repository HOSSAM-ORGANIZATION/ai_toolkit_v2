## Agent card

**LOADMAP tags:** `ui`, `clean-code`
**Read rest of this file:** no — this card contains the full enforceable rule.

### Must
- Use **Sealed Classes** (`sealed class ...`) for all Presentation States and Events to guarantee exhaustive compile-time pattern matching in widgets (`switch (state)`).
- Use **Records** (e.g. `(String name, int id)` or `({double lat, double lng})`) when passing or returning multiple transient values locally without creating single-use model classes.
- Use explicit class modifiers:
  - `interface class` for contracts that should only be implemented, never extended.
  - `abstract class` for hierarchies that share concrete member implementations.
  - `base class` when subclasses must inherit from a common base without arbitrary external implementation.
- **Intentionality Standard:** For every architectural choice or new abstraction, provide a 1-sentence rationale explaining why it is optimal. If a pragmatic temporary compromise is chosen, tag it: `// TODO: temporary trade-off - reason: <why>` and specify how it can be upgraded.

### Must not
- Use dynamic types or untyped maps in presentation state payloads.
- Forget the `default:` or catch-all branch when pattern matching sealed classes (allow the compiler to enforce exhaustiveness).
- Create boilerplate one-off DTO classes where a Dart 3 Record communicates the data structure more cleanly and with zero overhead.

### When to load the rest
- Only when designing complex pattern matching expressions or sealed class hierarchies.

### Related (cards first)
- `+state` for state machine design; `+patterns` for design pattern applications.

# Modern Dart 3+ Standards in Presentation & UI

## Purpose
Enforces the modern features of Dart 3+ (Sealed Classes, Records, Class Modifiers, Pattern Matching) to eliminate defensive boilerplate, guarantee exhaustiveness at compile time, and ensure complete transparency of code decisions.

## 1. Sealed Classes for Presentation State

All feature UI state hierarchies must be declared with `sealed class`. This allows widgets to consume state using exhaustive `switch` expressions without risk of unhandled states:

```dart
sealed class ProductDetailsState {}

final class ProductDetailsInitial extends ProductDetailsState {}
final class ProductDetailsLoading extends ProductDetailsState {}
final class ProductDetailsSuccess extends ProductDetailsState {
  final ProductEntity product;
  const ProductDetailsSuccess(this.product);
}
final class ProductDetailsFailure extends ProductDetailsState {
  final String message;
  const ProductDetailsFailure(this.message);
}

// Widget Consumption with Exhaustive Switch
Widget build(BuildContext context) {
  return switch (state) {
    ProductDetailsInitial() => const SizedBox.shrink(),
    ProductDetailsLoading() => const AppLoadingWidget(),
    ProductDetailsSuccess(:final product) => ProductView(product: product),
    ProductDetailsFailure(:final message) => AppFailWidget(message: message),
  };
}
```

## 2. Records for Transient Data

Use Dart Records to pair data or return multiple items from private helpers without polluting the codebase with micro-classes:

```dart
// Returning pagination boundaries cleanly
({int page, int pageSize}) calculatePagination() => (page: 1, pageSize: 20);

// Using named records for coordinate pairs or form validation
({bool isValid, String? error}) validateField(String input) {
  if (input.isEmpty) return (isValid: false, error: 'Field required');
  return (isValid: true, error: null);
}
```

## 3. Code Transparency & Intentionality

Every PR or feature code generation must provide clear answers:
1. **Why was this construct used?** (e.g. *Used a sealed class to enforce exhaustiveness across 4 distinct checkout phases*).
2. **Is it optimal?** (e.g. *Optimal because it prevents unhandled states at compile-time*).
3. **If a workaround:** (e.g. *// TODO: temporary trade-off - reason: Backend does not provide category IDs yet, using string slugs temporarily*).
