# Universal AI Toolkit v2 — Production ProGuard / R8 Rules for Flutter
# Protects Flutter engine, native plugins, serialization, Firebase, and payment gateways.

# --- Flutter Engine & Native JNI ---
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.**  { *; }
-keep class io.flutter.util.**  { *; }
-keep class io.flutter.view.**  { *; }
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }
-keep class io.flutter.plugin.editing.** { *; }
-dontwarn io.flutter.embedding.**

# --- Annotations & Attributes ---
-keepattributes *Annotation*
-keepattributes SourceFile,LineNumberTable
-keepattributes JavascriptInterface
-keepattributes InnerClasses,EnclosingMethod
-keepattributes Signature
-keepattributes Exceptions

# --- WebViews & Javascript Interface ---
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# --- Google Play Services, Billing & In-App Purchase ---
-keep class com.android.vending.billing.** { *; }
-keep class com.amazon.** { *; }
-dontwarn com.amazon.**
-keep class com.dooboolab.** { *; }

# --- Firebase & Google APIs ---
-keep class com.google.firebase.** { *; }
-dontwarn com.google.firebase.**
-keep class com.google.android.gms.** { *; }
-dontwarn com.google.android.gms.**

# --- JSON & Serialization (Gson / Moshi / Jackson) ---
-keepclassmembers enum * { *; }
-keepclassmembers class * implements java.io.Serializable {
    static final long serialVersionUID;
    private static final java.io.ObjectStreamField[] serialPersistentFields;
    !static !transient <fields>;
    !private <fields>;
    !private <methods>;
    private void writeObject(java.io.ObjectOutputStream);
    private void readObject(java.io.ObjectInputStream);
    java.lang.Object writeReplace();
    java.lang.Object readResolve();
}
-dontwarn com.google.gson.**
-keep class com.google.gson.** { *; }

# --- Networking (OkHttp / Retrofit) ---
-dontwarn okhttp3.**
-dontwarn okio.**
-dontwarn retrofit2.**
-keep class okhttp3.** { *; }

# --- Payment Gateways & Callbacks ---
-dontwarn com.razorpay.**
-keep class com.razorpay.** { *; }
-keepclasseswithmembers class * {
    public void onPayment*(...);
}
-optimizations !method/inlining/*
