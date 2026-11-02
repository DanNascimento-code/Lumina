import { Check, MessageCircleMore, ShieldCheck, ShoppingBag, Star, Truck, X } from 'lucide-react'
import { AnimatePresence, motion } from 'framer-motion'
import type { Product } from '../types'
import { formatCurrency } from '../lib/format'
import { useI18n } from '../i18n'

type Props = { product: Product | null; onClose: () => void; onAdd: (product: Product) => void; onAsk: (prompt: string) => void }

export function ProductModal({ product, onClose, onAdd, onAsk }: Props) {
  const { locale, t } = useI18n()
  return <AnimatePresence>{product && <motion.div className="modal-backdrop" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onMouseDown={onClose}>
    <motion.div className="product-modal" initial={{ opacity: 0, y: 28, scale: .98 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, y: 20 }} onMouseDown={(event) => event.stopPropagation()}>
      <button className="modal-close" onClick={onClose}><X /></button>
      <div className="product-modal-image" style={{ '--accent': product.accent } as React.CSSProperties}><img src={product.image_url} alt={product.name} /></div>
      <div className="product-modal-copy">
        <span className="modal-category">{t(`category.${product.category}`)}</span>
        <h2>{product.name}</h2>
        <div className="rating"><Star size={16} fill="currentColor" /> <b>{product.rating}</b> · {t('product.reviews', { count: product.review_count })}</div>
        <p>{product.description}</p>
        <div className="spec-grid">{Object.entries(product.specs).map(([key, value]) => <div key={key}><span>{key}</span><b>{value}</b></div>)}</div>
        <div className="modal-price"><strong>{formatCurrency(product.price, locale)}</strong><span>{t('product.installments', { value: formatCurrency(product.price / 10, locale) })}</span></div>
        <button className="btn btn-primary wide" onClick={() => { onAdd(product); onClose() }}><ShoppingBag size={19} /> {t('product.addCart')}</button>
        <button className="ask-product" onClick={() => { onClose(); onAsk(product.name) }}><MessageCircleMore /> {t('product.askLumi')}</button>
        <div className="mini-trust"><span><Truck /> {t('product.freeShipping')}</span><span><ShieldCheck /> {t('product.warranty')}</span><span><Check /> {t('product.returns')}</span></div>
      </div>
    </motion.div>
  </motion.div>}</AnimatePresence>
}
