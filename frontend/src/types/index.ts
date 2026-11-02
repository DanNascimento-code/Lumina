export type Product = {
  id: string
  slug: string
  name: string
  short_description: string
  description: string
  category: string
  price: number
  old_price?: number | null
  rating: number
  review_count: number
  stock: number
  image_url: string
  accent: string
  badges: string[]
  specs: Record<string, string>
}

export type CartItem = Product & { quantity: number }

export type Citation = { id: string; title: string; source: string; excerpt: string }
export type ChatAction = {
  type: 'view_product' | 'add_to_cart' | 'open_cart' | 'track_order'
  label: string
  product_id?: string
  product_name?: string
}
export type AssistantResponse = {
  message: string
  intent: string
  confidence: number
  grounded: boolean
  mode: 'live-rag' | 'local-rag' | 'safe-refusal'
  citations: Citation[]
  suggestions: string[]
  actions: ChatAction[]
  safety_notice?: string | null
}
export type ChatMessage = {
  id: string
  role: 'user' | 'assistant'
  content: string
  citations?: Citation[]
  suggestions?: string[]
  actions?: ChatAction[]
  mode?: AssistantResponse['mode']
}
