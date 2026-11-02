import { ArrowUpRight, Heart, Plus, Star } from 'lucide-react'
import { motion } from 'framer-motion'
import type { Product } from '../types'
import { formatCurrency } from '../lib/format'
import { useI18n } from '../i18n'

type Props = { product: Product; onAdd: (product: Product) => void; onView: (product: Product) => void }

export function ProductCard({ product, onAdd, onView }: Props) {
  const { locale, t } = useI18n()
  return <motion.article className="product-card" layout initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
    <button className="favorite" aria-label={t('product.favorite')}><Heart size={19} /></button>
    <div className="product-badges">{product.badges.map((badge) => <span key={badge}>{badge.startsWith('-') ? badge : t(`badge.${badge}`)}</span>)}</div>
    <button className="product-image-wrap" onClick={() => onView(product)} aria-label={t('product.view', { name: product.name })} style={{ '--accent': product.accent } as React.CSSProperties}>
      <img src={product.image_url} alt={product.name} loading="lazy" />
      <span className="quick-view">{t('product.details')} <ArrowUpRight size={15} /></span>
    </button>
    <div className="product-info">
      <div className="product-meta"><span>{t(`category.${product.category}`)}</span><span><Star size={13} fill="currentColor" /> {product.rating} <i>({product.review_count})</i></span></div>
      <h3>{product.name}</h3>
      <p>{product.short_description}</p>
      <div className="product-footer">
        <div className="price">{product.old_price && <del>{formatCurrency(product.old_price, locale)}</del>}<strong>{formatCurrency(product.price, locale)}</strong><small>{t('product.or', { value: formatCurrency(product.price / 10, locale) })}</small></div>
        <button className="add-button" onClick={() => onAdd(product)} aria-label={t('product.add', { name: product.name })}><Plus /></button>
      </div>
    </div>
  </motion.article>
}
