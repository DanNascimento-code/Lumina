import { useEffect, useMemo, useState } from 'react'
import type { CartItem, Product } from '../types'

const STORAGE_KEY = 'lumina-cart-v1'

export function useCart() {
  const [items, setItems] = useState<CartItem[]>(() => {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') }
    catch { return [] }
  })

  useEffect(() => localStorage.setItem(STORAGE_KEY, JSON.stringify(items)), [items])

  const add = (product: Product, quantity = 1) => setItems((current) => {
    const found = current.find((item) => item.id === product.id)
    if (found) return current.map((item) => item.id === product.id
      ? { ...item, quantity: Math.min(item.quantity + quantity, item.stock) } : item)
    return [...current, { ...product, quantity }]
  })
  const remove = (id: string) => setItems((current) => current.filter((item) => item.id !== id))
  const update = (id: string, quantity: number) => setItems((current) => current.map((item) =>
    item.id === id ? { ...item, quantity: Math.max(1, Math.min(quantity, item.stock)) } : item))
  const clear = () => setItems([])
  const count = useMemo(() => items.reduce((sum, item) => sum + item.quantity, 0), [items])
  const subtotal = useMemo(() => items.reduce((sum, item) => sum + item.price * item.quantity, 0), [items])
  return { items, add, remove, update, clear, count, subtotal }
}
