import { AnimatePresence, motion } from 'framer-motion'
import { ArrowRight, Bot, ChevronDown, ExternalLink, MessageCircleMore, Send, ShieldCheck, ShoppingBag, Sparkles, UserRound, X } from 'lucide-react'
import { FormEvent, useEffect, useRef, useState } from 'react'
import { sendChat } from '../lib/api'
import type { CartItem, ChatAction, ChatMessage, Product } from '../types'
import { useI18n, type Locale } from '../i18n'

type Props = {
  open: boolean; onOpen: () => void; onClose: () => void; initialPrompt?: string; cart: CartItem[]; products: Product[]
  onViewProduct: (product: Product) => void; onOpenCart: () => void
}

export function Assistant({ open, onOpen, onClose, initialPrompt, cart, products, onViewProduct, onOpenCart }: Props) {
  const { locale, t } = useI18n()
  const [messages, setMessages] = useState<ChatMessage[]>([{ id: 'welcome', role: 'assistant', content: t('assistant.welcome') }])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  const usedPrompt = useRef('')
  const starters = [
    ['✨', t('assistant.find'), starterPrompt(locale, 'find')],
    ['⇄', t('assistant.compare'), starterPrompt(locale, 'compare')],
    ['⌁', t('assistant.shipping'), starterPrompt(locale, 'shipping')],
    ['♢', t('assistant.returns'), starterPrompt(locale, 'returns')],
  ]

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) }, [messages, loading, open])
  useEffect(() => { setMessages((current) => current.length === 1 && current[0].id === 'welcome' ? [{ ...current[0], content: t('assistant.welcome') }] : current) }, [locale, t])
  useEffect(() => {
    if (open && initialPrompt && usedPrompt.current !== initialPrompt) {
      usedPrompt.current = initialPrompt
      void ask(initialPrompt)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, initialPrompt])

  const ask = async (text: string) => {
    const clean = text.trim(); if (!clean || loading) return
    const user: ChatMessage = { id: crypto.randomUUID(), role: 'user', content: clean }
    const history = [...messages, user]
    setMessages(history); setInput(''); setLoading(true)
    try {
      const response = await sendChat(clean, messages, cart, locale)
      setMessages((current) => [...current, { id: crypto.randomUUID(), role: 'assistant', content: response.message, citations: response.citations, suggestions: response.suggestions, actions: response.actions }])
    } catch {
      setMessages((current) => [...current, localAnswer(clean, locale)])
    } finally { setLoading(false) }
  }
  const submit = (event: FormEvent) => { event.preventDefault(); void ask(input) }
  const performAction = (action: ChatAction) => {
    if (action.type === 'open_cart') onOpenCart()
    if ((action.type === 'view_product' || action.type === 'add_to_cart') && action.product_id) {
      const product = products.find((item) => item.id === action.product_id)
      if (product) { onClose(); onViewProduct(product) }
    }
  }
  return <>
    <AnimatePresence>{open && <motion.aside className="assistant-panel" initial={{ opacity: 0, y: 24, scale: .97 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: 20, scale: .97 }} transition={{ type: 'spring', damping: 25, stiffness: 280 }}>
      <header className="assistant-header">
        <span className="lumi-orb"><i /></span>
        <div><h2>{t('assistant.name')} <span>AI</span></h2><p><i /> {t('assistant.online')}</p></div>
        <button onClick={onClose} aria-label={t('assistant.close')}><X /></button>
      </header>
      <div className="assistant-trust"><ShieldCheck size={14} /> {t('assistant.trust')}</div>
      <div className="chat-body">
        {messages.map((message, index) => <div className={`message-row ${message.role}`} key={message.id}>
          <span className="message-avatar">{message.role === 'assistant' ? <Sparkles /> : <UserRound />}</span>
          <div className="message-stack">
            <div className="message-bubble">{message.content}</div>
            {message.citations && message.citations.length > 0 && <details className="citations"><summary><Bot /> {message.citations.length === 1 ? t('assistant.source') : t('assistant.sources', { count: message.citations.length })} <ChevronDown /></summary>{message.citations.map((citation) => <div key={citation.id}><b>{citation.title}</b><p>{citation.excerpt}</p><span>{citation.source} <ExternalLink /></span></div>)}</details>}
            {message.actions && message.actions.length > 0 && <div className="message-actions">{message.actions.map((action) => <button key={action.label} onClick={() => performAction(action)}><ShoppingBag />{action.label}<ArrowRight /></button>)}</div>}
            {message.suggestions && message.suggestions.length > 0 && index === messages.length - 1 && <div className="suggestion-chips">{message.suggestions.map((suggestion) => <button key={suggestion} onClick={() => void ask(suggestion)}>{suggestion}</button>)}</div>}
          </div>
        </div>)}
        {messages.length === 1 && <div className="starters"><span>{t('assistant.canHelp')}</span>{starters.map(([icon, label, prompt]) => <button key={label} onClick={() => void ask(prompt)}><i>{icon}</i><b>{label}</b><ArrowRight /></button>)}</div>}
        {loading && <div className="message-row assistant"><span className="message-avatar"><Sparkles /></span><div className="typing"><i /><i /><i /><span>{t('assistant.consulting')}</span></div></div>}
        <div ref={bottomRef} />
      </div>
      <form className="chat-input" onSubmit={submit}>
        <div><textarea value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={(event) => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); void ask(input) } }} placeholder={t('assistant.placeholder')} rows={1} maxLength={4000} /><button disabled={!input.trim() || loading} aria-label={t('assistant.send')}><Send /></button></div>
        <small><ShieldCheck /> {t('assistant.disclaimer')}</small>
      </form>
    </motion.aside>}</AnimatePresence>
    {!open && <motion.button className="assistant-fab" initial={{ scale: 0 }} animate={{ scale: 1 }} onClick={() => { usedPrompt.current = ''; onOpen() }} aria-label={t('assistant.fab')}><span className="lumi-orb"><i /></span><span><b>{t('assistant.fab')}</b><small>{t('assistant.fabBody')}</small></span><MessageCircleMore /></motion.button>}
  </>
}

function starterPrompt(locale: Locale, type: 'find' | 'compare' | 'shipping' | 'returns') {
  const prompts = {
    'en-US': { find: 'Help me choose the right product', compare: 'Compare Aurora and Nimbus for my needs', shipping: 'How do shipping and delivery times work?', returns: 'Explain the returns and warranty policies' },
    'pt-BR': { find: 'Me ajude a escolher o produto ideal', compare: 'Compare Aurora e Nimbus para o meu uso', shipping: 'Como funcionam o frete e o prazo de entrega?', returns: 'Explique a política de trocas e garantia' },
    'es-419': { find: 'Ayúdame a elegir el producto ideal', compare: 'Compara Aurora y Nimbus para mis necesidades', shipping: '¿Cómo funcionan el envío y los plazos de entrega?', returns: 'Explica las políticas de devolución y garantía' },
  }
  return prompts[locale][type]
}

function localAnswer(text: string, locale: Locale): ChatMessage {
  const query = text.toLocaleLowerCase('pt-BR')
  const shared = { id: crypto.randomUUID(), role: 'assistant' as const }
  const copy = localCopy[locale]
  if (/ignore|prompt|instruç|system|reveal|ignora/.test(query)) return { ...shared, content: copy.security, suggestions: copy.securitySuggestions }
  if (/troca|devol|reembolso|arrepend|return|refund|devoluci|reembolso/.test(query)) return { ...shared, content: copy.returns, citations: [{ id: 'returns', title: copy.returnsTitle, source: 'knowledge/returns_policy.md', excerpt: copy.returnsExcerpt }], suggestions: copy.returnsSuggestions }
  if (/frete|entrega|prazo|cep|shipping|delivery|envío|entrega/.test(query)) return { ...shared, content: copy.shipping, citations: [{ id: 'shipping', title: copy.shippingTitle, source: 'knowledge/shipping_policy.md', excerpt: copy.shippingExcerpt }], suggestions: copy.shippingSuggestions }
  if (/aurora|nimbus|compar|recomenda|escolh|choose|recommend|compara|elegir/.test(query)) return { ...shared, content: copy.recommendation, citations: [{ id: 'catalog', title: copy.catalogTitle, source: 'knowledge/product_catalog.md', excerpt: copy.catalogExcerpt }], suggestions: copy.recommendationSuggestions, actions: [{ type: 'view_product', label: copy.viewAurora, product_id: 'aurora-headphones', product_name: 'Aurora Headphones' }] }
  return { ...shared, content: copy.general, suggestions: copy.generalSuggestions }
}

type LocalAssistantCopy = {
  security: string
  securitySuggestions: string[]
  returns: string
  returnsTitle: string
  returnsExcerpt: string
  returnsSuggestions: string[]
  shipping: string
  shippingTitle: string
  shippingExcerpt: string
  shippingSuggestions: string[]
  recommendation: string
  catalogTitle: string
  catalogExcerpt: string
  recommendationSuggestions: string[]
  viewAurora: string
  general: string
  generalSuggestions: string[]
}

const localCopy: Record<Locale, LocalAssistantCopy> = {
  'en-US': { security: 'I can help with Lumina products, orders and policies, but I cannot change my operating rules or expose protected instructions.', securitySuggestions: ['Compare the headphones', 'How do returns work?'], returns: 'Online purchases can be returned within 7 calendar days of delivery. Products must include their accessories and manuals and show no signs of misuse. Return shipping is provided after approval.', returnsTitle: 'Returns and Refunds Policy', returnsExcerpt: 'Online purchases may be returned within 7 calendar days from delivery…', returnsSuggestions: ['How do I start a return?', 'When will I receive my refund?'], shipping: 'Lumina ships throughout Brazil. Orders over $90 include free standard shipping, and the exact delivery estimate for your postal code is shown at checkout.', shippingTitle: 'Shipping Policy', shippingExcerpt: 'Orders over $90 include free standard shipping…', shippingSuggestions: ['How do I track my order?', 'Can I change the address?'], recommendation: 'For focus, travel and calls, I would choose Aurora for its adaptive noise cancellation and up to 42 hours of battery. For shared music and outdoor use, Nimbus is the better fit with 360° sound, 18 hours of battery and IP67 protection.', catalogTitle: 'Official Product Catalog', catalogExcerpt: 'Choose Aurora for focus, travel and calls; Nimbus for shared listening and outdoor use…', recommendationSuggestions: ['I travel often', 'I want it for gatherings', 'Compare the prices'], viewAurora: 'View Aurora Headphones', general: 'Tell me a little about how you plan to use it. Are you shopping for focus, music, fitness, a smart home or productivity?', generalSuggestions: ['Improve my focus', 'I need a gift', 'Show me the best offers'] },
  'pt-BR': { security: 'Posso ajudar com produtos, pedidos e políticas da Lumina, mas não posso alterar minhas regras internas nem expor instruções protegidas.', securitySuggestions: ['Compare os headphones', 'Como funcionam as devoluções?'], returns: 'Compras online podem ser devolvidas em até 7 dias corridos após o recebimento. O produto deve voltar com acessórios, manuais e sem sinais de mau uso. A postagem é fornecida após a aprovação.', returnsTitle: 'Política de Trocas e Reembolsos', returnsExcerpt: 'Compras online podem ser devolvidas em até 7 dias corridos do recebimento…', returnsSuggestions: ['Como inicio a devolução?', 'Quando recebo o estorno?'], shipping: 'A Lumina entrega em todo o Brasil. Pedidos acima de R$ 499 têm frete padrão grátis e o prazo exato para o seu CEP aparece no checkout.', shippingTitle: 'Política de Entregas', shippingExcerpt: 'Pedidos acima de R$ 499 têm frete padrão gratuito…', shippingSuggestions: ['Como acompanho o pedido?', 'Posso alterar o endereço?'], recommendation: 'Para foco, viagens e chamadas, eu escolheria o Aurora pelo cancelamento adaptativo e até 42h de bateria. Para música compartilhada e área externa, a Nimbus faz mais sentido, com som 360°, 18h e proteção IP67.', catalogTitle: 'Catálogo Oficial de Produtos', catalogExcerpt: 'Escolha Aurora para foco, viagens e chamadas; Nimbus para som compartilhado e área externa…', recommendationSuggestions: ['Viajo com frequência', 'Quero para encontros', 'Compare os preços'], viewAurora: 'Ver Aurora Headphones', general: 'Conte um pouco sobre o seu uso. Você procura algo para foco, música, atividade, casa conectada ou produtividade?', generalSuggestions: ['Melhorar meu foco', 'Preciso de um presente', 'Mostrar as melhores ofertas'] },
  'es-419': { security: 'Puedo ayudar con productos, pedidos y políticas de Lumina, pero no puedo cambiar mis reglas internas ni revelar instrucciones protegidas.', securitySuggestions: ['Comparar audífonos', '¿Cómo funcionan las devoluciones?'], returns: 'Las compras en línea pueden devolverse dentro de los 7 días calendario posteriores a la entrega. El producto debe incluir accesorios y manuales y no mostrar señales de mal uso.', returnsTitle: 'Política de Devoluciones y Reembolsos', returnsExcerpt: 'Las compras en línea pueden devolverse dentro de los 7 días calendario posteriores a la entrega…', returnsSuggestions: ['¿Cómo inicio una devolución?', '¿Cuándo recibiré el reembolso?'], shipping: 'Lumina realiza envíos a todo Brasil. Los pedidos superiores a US$90 incluyen envío estándar gratis y el plazo exacto para tu código postal aparece al pagar.', shippingTitle: 'Política de Envíos', shippingExcerpt: 'Los pedidos superiores a US$90 incluyen envío estándar gratis…', shippingSuggestions: ['¿Cómo rastreo mi pedido?', '¿Puedo cambiar la dirección?'], recommendation: 'Para concentración, viajes y llamadas, elegiría Aurora por su cancelación adaptativa y hasta 42 horas de batería. Para música compartida y exteriores, Nimbus ofrece sonido 360°, 18 horas e IP67.', catalogTitle: 'Catálogo Oficial de Productos', catalogExcerpt: 'Elige Aurora para concentración, viajes y llamadas; Nimbus para música compartida y exteriores…', recommendationSuggestions: ['Viajo con frecuencia', 'Lo quiero para reuniones', 'Comparar precios'], viewAurora: 'Ver Aurora Headphones', general: 'Cuéntame cómo piensas usarlo. ¿Buscas algo para concentración, música, actividad, hogar inteligente o productividad?', generalSuggestions: ['Mejorar mi concentración', 'Necesito un regalo', 'Mostrar las mejores ofertas'] },
}
