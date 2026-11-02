import { Minus, Plus, ShoppingBag, Trash2, Truck, X } from 'lucide-react'
import { AnimatePresence, motion } from 'framer-motion'
import type { CartItem } from '../types'
import { formatCurrency } from '../lib/format'
import { useI18n } from '../i18n'

type Props = {
  open: boolean; items: CartItem[]; subtotal: number
  onClose: () => void; onRemove: (id: string) => void; onUpdate: (id: string, quantity: number) => void
  onCheckout: () => void
}

export function CartDrawer({ open, items, subtotal, onClose, onRemove, onUpdate, onCheckout }: Props) {
  const { locale, t } = useI18n()
  const missing = Math.max(0, 499 - subtotal)
  return <AnimatePresence>{open && <>
    <motion.button className="drawer-backdrop" aria-label={t('cart.close')} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose} />
    <motion.aside className="cart-drawer" initial={{ x: '100%' }} animate={{ x: 0 }} exit={{ x: '100%' }} transition={{ type: 'spring', damping: 28, stiffness: 260 }}>
      <div className="drawer-header"><div><small>{t('cart.title')}</small><h2>{items.length ? t(items.length === 1 ? 'cart.product' : 'cart.products', { count: items.length }) : t('cart.empty')}</h2></div><button onClick={onClose} aria-label={t('cart.close')}><X /></button></div>
      {items.length > 0 && <div className="shipping-progress">
        <div><Truck size={17} /><span>{missing > 0 ? t('cart.freeMissing', { value: formatCurrency(missing, locale) }) : <b>{t('cart.freeEarned')}</b>}</span></div>
        <i><span style={{ width: `${Math.min(100, subtotal / 499 * 100)}%` }} /></i>
      </div>}
      <div className="cart-items">{items.length === 0 ? <div className="empty-cart"><span><ShoppingBag /></span><h3>{t('cart.emptyTitle')}</h3><p>{t('cart.emptyBody')}</p><button className="btn btn-primary" onClick={onClose}>{t('cart.explore')}</button></div> : items.map((item) => <article className="cart-item" key={item.id}>
        <img src={item.image_url} alt={item.name} />
        <div><span>{t(`category.${item.category}`)}</span><h3>{item.name}</h3><b>{formatCurrency(item.price, locale)}</b>
          <div className="quantity"><button onClick={() => onUpdate(item.id, item.quantity - 1)}><Minus /></button><span>{item.quantity}</span><button onClick={() => onUpdate(item.id, item.quantity + 1)}><Plus /></button></div>
        </div>
        <button className="remove-item" onClick={() => onRemove(item.id)} aria-label={t('cart.remove', { name: item.name })}><Trash2 /></button>
      </article>)}</div>
      {items.length > 0 && <div className="cart-summary">
        <div><span>{t('cart.subtotal')}</span><b>{formatCurrency(subtotal, locale)}</b></div>
        <div><span>{t('cart.shipping')}</span><b className="free">{subtotal >= 499 ? t('cart.free') : t('cart.calculated')}</b></div>
        <button className="btn btn-primary wide" onClick={onCheckout}>{t('cart.checkout')} <span>→</span></button>
        <small>{t('cart.secure')}</small>
      </div>}
    </motion.aside>
  </>}</AnimatePresence>
}
