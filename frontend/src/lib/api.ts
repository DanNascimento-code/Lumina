import type { AssistantResponse, CartItem, ChatMessage, Product } from '../types'
import type { Locale } from '../i18n'

const API_URL = import.meta.env.VITE_API_URL || '/api/v1'

export async function fetchProducts(): Promise<Product[]> {
  const response = await fetch(`${API_URL}/products`, { signal: AbortSignal.timeout(3500) })
  if (!response.ok) throw new Error('Catalog unavailable')
  return response.json()
}

export async function sendChat(
  message: string,
  history: ChatMessage[],
  cart: CartItem[],
  locale: Locale,
): Promise<AssistantResponse> {
  const response = await fetch(`${API_URL}/assistant/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      locale,
      session_id: getSessionId(),
      history: history.slice(-8).map(({ role, content }) => ({ role, content })),
      cart: cart.map(({ id, name, quantity, price }) => ({ product_id: id, name, quantity, price })),
    }),
    signal: AbortSignal.timeout(25000),
  })
  if (!response.ok) throw new Error('Assistant unavailable')
  return response.json()
}

export async function submitCheckout(payload: Record<string, unknown>) {
  const response = await fetch(`${API_URL}/orders/checkout`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(10000),
  })
  if (!response.ok) throw new Error('The order could not be completed')
  return response.json()
}

function getSessionId() {
  const existing = sessionStorage.getItem('lumina-session')
  if (existing) return existing
  const id = crypto.randomUUID()
  sessionStorage.setItem('lumina-session', id)
  return id
}
