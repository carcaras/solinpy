from __future__ import annotations

from typing import Any, Mapping, Optional


def _format_context(context: Mapping[str, Any] | None) -> str:
    if not context:
        return ""

    parts = [f"{key}={value}" for key, value in context.items() if value is not None]
    return ", ".join(parts)


def _friendly_rpc_message(method: str, code: Optional[int], message: str) -> str:
    normalized = message.lower()

    if code == -32600 or "invalid request" in normalized:
        return "Requisição RPC inválida. Verifique os parâmetros enviados."

    if code == -32601 or "method not found" in normalized:
        return f"Método RPC desconhecido em {method}. Verifique o nome da operação."

    if code == -32602 or any(
        term in normalized for term in ("invalid params", "invalid parameter", "invalid argument")
    ):
        return f"Parâmetros inválidos ao executar {method}. Revise os valores enviados."

    if any(term in normalized for term in ("insufficient funds", "insufficient balance")):
        return (
            f"Saldo insuficiente ao executar {method}. "
            "Verifique se a conta tem SOL suficiente para taxas e valor da operação."
        )

    if any(
        term in normalized
        for term in (
            "account not found",
            "invalid account",
            "could not find account",
            "failed to get account info",
            "account does not exist",
        )
    ):
        return f"Conta inválida ou inexistente ao executar {method}. Verifique o endereço informado."

    if any(term in normalized for term in ("blockhash not found", "blockhash expired")):
        return f"Blockhash expirado ou inválido ao executar {method}. Busque um blockhash novo e tente novamente."

    if code in (-32004, -32005):
        return f"Serviço RPC temporariamente indisponível ao executar {method}. Tente novamente em instantes."

    if message:
        return f"Erro RPC ao executar {method}: {message}"

    return f"Erro RPC ao executar {method}."


class RPCError(Exception):
    """Erro de RPC com mensagem amigável e contexto estruturado."""

    def __init__(
        self,
        message: str,
        *,
        code: Optional[int] = None,
        method: Optional[str] = None,
        context: Optional[Mapping[str, Any]] = None,
        cause: Optional[BaseException] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.method = method
        self.context = dict(context or {})
        self.cause = cause

    def __str__(self) -> str:
        details: list[str] = []
        if self.code is not None:
            details.append(f"código RPC={self.code}")
        if self.method is not None:
            details.append(f"método={self.method}")

        context_text = _format_context(self.context)
        if context_text:
            details.append(f"contexto={context_text}")

        if self.cause is not None:
            details.append(f"causa={self.cause}")

        if not details:
            return self.message

        return f"{self.message} [{' | '.join(details)}]"

    @classmethod
    def from_rpc_error(
        cls,
        method: str,
        rpc_error: Mapping[str, Any],
        *,
        context: Optional[Mapping[str, Any]] = None,
    ) -> "RPCError":
        code = rpc_error.get("code")
        raw_message = str(rpc_error.get("message") or "")
        friendly_message = _friendly_rpc_message(method, code if isinstance(code, int) else None, raw_message)

        extra_details = rpc_error.get("data")
        merged_context: dict[str, Any] = dict(context or {})
        if extra_details is not None:
            merged_context["rpc_data"] = extra_details

        return cls(
            friendly_message,
            code=code if isinstance(code, int) else None,
            method=method,
            context=merged_context,
        )

    @classmethod
    def from_transport_error(
        cls,
        method: str,
        error: BaseException,
        *,
        context: Optional[Mapping[str, Any]] = None,
        message: Optional[str] = None,
    ) -> "RPCError":
        friendly_message = message or f"Falha de comunicação ao executar {method}. Verifique o endpoint e tente novamente."
        return cls(friendly_message, method=method, context=context, cause=error)
