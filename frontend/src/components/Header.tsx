import { Heart, Menu, Search, ShoppingBag, UserRound, X } from 'lucide-react'
import { useState } from 'react'
import { useI18n, type Locale } from '../i18n'

type Props = {
  cartCount: number
  search: string
  onSearch: (value: string) => void
  onCart: () => void
}

export function Header({ cartCount, search, onSearch, onCart }: Props) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const { locale, setLocale, t } = useI18n()
  return <>
    <div className="announcement">
      <span>{t('announcement.shipping')}</span>
      <span className="announcement-dot" />
      <span>{t('announcement.installments')}</span>
      <a href="#benefits">{t('announcement.club')} <span>↗</span></a>
    </div>
    <header className="site-header">
      <button className="icon-btn menu-btn" aria-label={t('header.menu')} onClick={() => setMobileOpen(true)}><Menu /></button>
      <a className="brand" href="#top" aria-label="Lumina home">
        <span className="brand-mark"><i /><i /></span><b>LUMINA</b>
      </a>
      <nav className={mobileOpen ? 'nav open' : 'nav'} aria-label={t('header.navigation')}>
        <button className="nav-close" onClick={() => setMobileOpen(false)} aria-label={t('header.closeMenu')}><X /></button>
        <a href="#new-arrivals">{t('nav.new')}</a>
        <a href="#products">{t('nav.products')}</a>
        <a href="#collections">{t('nav.collections')}</a>
        <a href="#offers">{t('nav.offers')} <span className="nav-pill">{t('nav.hot')}</span></a>
      </nav>
      <div className="header-actions">
        <label className="search-box">
          <Search size={18} />
          <input value={search} onChange={(event) => onSearch(event.target.value)} placeholder={t('header.search')} />
          <kbd>⌘ K</kbd>
        </label>
        <label className="language-select" aria-label={t('language.label')}>
          <span>{locale === 'en-US' ? 'EN' : locale === 'pt-BR' ? 'PT' : 'ES'}</span>
          <select value={locale} onChange={(event) => setLocale(event.target.value as Locale)}>
            <option value="en-US">{t('language.en')}</option><option value="pt-BR">{t('language.pt')}</option><option value="es-419">{t('language.es')}</option>
          </select>
        </label>
        <button className="icon-btn hide-mobile" aria-label={t('header.favorites')}><Heart /></button>
        <button className="icon-btn hide-mobile" aria-label={t('header.account')}><UserRound /></button>
        <button className="icon-btn cart-button" aria-label={t('header.cart', { count: cartCount })} onClick={onCart}>
          <ShoppingBag />{cartCount > 0 && <span>{cartCount}</span>}
        </button>
      </div>
    </header>
  </>
}
