#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Core Network Interceptors & Failures Setup Engine
Scaffolds production-grade Dio interceptors (Headers, 401 Logout) and Clean Architecture Failure mappers.
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
from pathlib import Path

def setup_network_interceptors(target_dir="."):
    target_path = Path(target_dir).resolve()
    lib_dir = target_path / "lib"
    net_dir = lib_dir / "core" / "network"
    interceptors_dir = net_dir / "interceptors"
    errors_dir = net_dir / "errors"

    interceptors_dir.mkdir(parents=True, exist_ok=True)
    errors_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "🌐"*35)
    print("  UNIVERSAL AI TOOLKIT v2 — NETWORK INTERCEPTORS SETUP")
    print("🌐"*35)
    print(f"📂 Project Root: {target_path}")

    # 1. ApiHeaderInterceptor
    header_file = interceptors_dir / "api_header_interceptor.dart"
    if not header_file.exists():
        with open(header_file, "w", encoding="utf-8") as f:
            f.write("""import 'package:dio/dio.dart';

/// Injects standard headers: Accept, Accept-Language, and Bearer token into outgoing requests.
class ApiHeaderInterceptor extends Interceptor {
  final Future<String?> Function()? getToken;
  final String Function()? getLanguage;

  ApiHeaderInterceptor({this.getToken, this.getLanguage});

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    options.headers['Accept'] = 'application/json';
    
    // Inject active language (default: ar)
    final lang = getLanguage != null ? getLanguage!() : 'ar';
    options.headers['Accept-Language'] = lang;

    // Inject Bearer Token if available
    if (getToken != null) {
      final token = await getToken!();
      if (token != null && token.isNotEmpty) {
        options.headers['Authorization'] = 'Bearer $token';
      }
    }

    return handler.next(options);
  }
}
""")
        print("   ✅ Created: lib/core/network/interceptors/api_header_interceptor.dart")

    # 2. UnauthenticatedInterceptor (401 Handler)
    auth_file = interceptors_dir / "unauthenticated_interceptor.dart"
    if not auth_file.exists():
        with open(auth_file, "w", encoding="utf-8") as f:
            f.write("""import 'package:dio/dio.dart';

/// Intercepts 401 Unauthorized responses to trigger token revocation and navigation.
class UnauthenticatedInterceptor extends Interceptor {
  final Future<void> Function()? onSessionExpired;

  UnauthenticatedInterceptor({this.onSessionExpired});

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      if (onSessionExpired != null) {
        await onSessionExpired!();
      }
    }
    return handler.next(err);
  }
}
""")
        print("   ✅ Created: lib/core/network/interceptors/unauthenticated_interceptor.dart")

    # 3. Failures
    failures_file = errors_dir / "failures.dart"
    if not failures_file.exists():
        with open(failures_file, "w", encoding="utf-8") as f:
            f.write("""import 'package:equatable/equatable.dart';

abstract class Failure extends Equatable {
  final String message;
  final int? statusCode;

  const Failure({required this.message, this.statusCode});

  @override
  List<Object?> get props => [message, statusCode];
}

class ServerFailure extends Failure {
  const ServerFailure({required super.message, super.statusCode});
}

class NetworkFailure extends Failure {
  const NetworkFailure({required super.message, super.statusCode});
}

class AuthFailure extends Failure {
  const AuthFailure({required super.message, super.statusCode});
}

class ValidationFailure extends Failure {
  final Map<String, dynamic>? errors;
  const ValidationFailure({required super.message, this.errors, super.statusCode});
}
""")
        print("   ✅ Created: lib/core/network/errors/failures.dart")

    # 4. ExceptionMapper
    mapper_file = errors_dir / "exception_mapper.dart"
    if not mapper_file.exists():
        with open(mapper_file, "w", encoding="utf-8") as f:
            f.write("""import 'package:dio/dio.dart';
import 'failures.dart';

class ExceptionMapper {
  static Failure mapDioException(DioException exception) {
    switch (exception.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.connectionError:
        return const NetworkFailure(
          message: 'تعذر الاتصال بالخادم، يرجى التحقق من اتصال الإنترنت.',
        );

      case DioExceptionType.badResponse:
        final code = exception.response?.statusCode;
        final data = exception.response?.data;
        String message = 'حدث خطأ غير متوقع، يرجى المحاولة لاحقاً.';

        if (data is Map && data['message'] != null) {
          message = data['message'].toString();
        }

        if (code == 401) {
          return AuthFailure(message: message, statusCode: code);
        } else if (code == 422) {
          return ValidationFailure(message: message, statusCode: code);
        } else {
          return ServerFailure(message: message, statusCode: code);
        }

      default:
        return const ServerFailure(
          message: 'حدث خطأ في معالجة الطلب، يرجى المحاولة مجدداً.',
        );
    }
  }
}
""")
        print("   ✅ Created: lib/core/network/errors/exception_mapper.dart")

    print("\n🎉 Core network interceptors & failure mappers setup completed successfully!")
    print("="*70 + "\n")
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
    setup_network_interceptors(target)
