# vidaplus/logger.py
import logging

class VidaPlusLogger:
    def __init__(self, module_name: str):
        self.logger = logging.getLogger(f"vidaplus.{module_name}")
        self.module_name = module_name
    
    def _log_with_context(self, level: str, message: str, **context):
        """Método base para logs com contexto"""
        safe_context = {}
        for key, value in context.items():
            if key in ['module', 'name', 'msg', 'args', 'levelname', 'levelno', 
                      'pathname', 'filename', 'exc_info', 'exc_text', 'stack_info', 
                      'lineno', 'funcName', 'created', 'msecs', 'relativeCreated', 
                      'thread', 'threadName', 'processName', 'process']:
                safe_context[f"ctx_{key}"] = value
            else:
                safe_context[key] = value
        
        safe_context['service_module'] = self.module_name
        
        context_str = " | ".join([f"{k}={v}" for k, v in safe_context.items() if not k.startswith('_')])
        full_message = f"{message} | {context_str}" if context_str else message
        
        getattr(self.logger, level)(full_message, extra=safe_context)
    
    def resource_not_found(self, resource_type: str, resource_id: str, user_id: str, operation: str):
        self._log_with_context(
            "warning",
            f"{resource_type} não encontrado",
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            operation=operation,
            log_type="resource_not_found"
        )
    
    def business_conflict(self, conflict_type: str, details: str, user_id: str, **extra):
        self._log_with_context(
            "warning",
            "Conflito de negócio: {conflict_type}",
            conflict_type=conflict_type,
            details=details,
            user_id=user_id,
            log_type="business_conflict",
            **extra
        )
    
    def operation_success(self, operation: str, resource_id: str, user_id: str, **extra):
        self._log_with_context(
            "info",
            "Operação realizada com sucesso",
            operation=operation,
            resource_id=resource_id,
            user_id=user_id,
            log_type="operation_success",
            **extra
        )
    
    def permission_denied(self, operation: str, resource_id: str, user_id: str, reason: str):
        self._log_with_context(
            "warning",
            "Acesso negado",
            operation=operation,
            resource_id=resource_id,
            user_id=user_id,
            reason=reason,
            log_type="permission_denied"
        )
    
    def error(self, operation: str, error_message: str, user_id: str, **extra):
        self._log_with_context(
            "error",
            "Erro na operação",
            operation=operation,
            error_message=error_message,
            user_id=user_id,
            log_type="error",
            **extra
        )

def get_logger(module_name: str) -> VidaPlusLogger:
    return VidaPlusLogger(module_name)