import { ArrowRight, Box, Headphones, Home, Keyboard, RotateCcw, ShieldCheck, Sparkles, Truck, Watch } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Assistant } from './components/Assistant'
import { CartDrawer } from './components/CartDrawer'
import { CheckoutFlow } from './components/CheckoutFlow'
import { Header } from './components/Header'
import { Hero } from './components/Hero'
import { ProductCard } from './components/ProductCard'
import { ProductModal } from './components/ProductModal'
import { categories, localizeProduct, products as fallbackProducts } from './data/products'
import { useCart } from './hooks/useCart'
import { fetchProducts } from './lib/api'
import type { Product } from './types'
import { useI18n } from './i18n'

const categoryIcons = [Sparkles, Headphones, Watch, Home, Keyboard, Box]

export default function App() {
  const { locale, t } = useI18n()
  const [products, setProducts] = useState<Product[]>(fallbackProducts)
  const [category, setCategory] = useState('All')
  const [search, setSearch] = useState('')
  const [cartOpen, setCartOpen] = useState(false)
  const [checkoutOpen, setCheckoutOpen] = useState(false)
  const [assistantOpen, setAssistantOpen] = useState(() => window.matchMedia('(min-width: 900px)').matches)
  const [assistantPrompt, setAssistantPrompt] = useState<string>()
  const [selected, setSelected] = useState<Product | null>(null)
  const [toast, setToast] = useState('')
  const cart = useCart()

  useEffect(() => { fetchProducts().then(setProducts).catch(() => undefined) }, [])
  useEffect(() => { if (toast) { const id = setTimeout(() => setToast(''), 2400); return () => clearTimeout(id) } }, [toast])

  const localizedProducts = useMemo(() => products.map((product) => localizeProduct(product, locale)), [products, locale])
  const visible = useMemo(() => localizedProducts.filter((product) =>
    (category === 'All' || product.category === category) &&
    (!search || `${product.name} ${product.category} ${product.short_description}`.toLocaleLowerCase('pt-BR').includes(search.toLocaleLowerCase('pt-BR')))
  ), [localizedProducts, category, search])

  const addProduct = (product: Product) => { cart.add(product); setToast(t('toast.added', { name: product.name })) }
  const askLumi = (prompt?: string) => { setAssistantPrompt(prompt); setAssistantOpen(true) }
  const startCheckout = () => { setCartOpen(false); setCheckoutOpen(true) }

  return <div className="app">
    <Header cartCount={cart.count} search={search} onSearch={setSearch} onCart={() => setCartOpen(true)} />
    <main>
      <Hero onAskLumi={askLumi} />
      <section className="category-rail" id="collections">
        <div className="section-intro"><span>{t('categories.eyebrow')}</span><h2>{t('categories.title')}</h2></div>
        <div className="category-list">{categories.map((item, index) => { const Icon = categoryIcons[index]; const count = item === 'All' ? products.length : products.filter((p) => p.category === item).length; return <button key={item} className={category === item ? 'active' : ''} onClick={() => { setCategory(item); document.querySelector('#products')?.scrollIntoView({ behavior: 'smooth' }) }}><span><Icon /></span><b>{t(`category.${item}`)}</b><small>{t(count === 1 ? 'categories.one' : 'categories.count', { count })}</small></button> })}</div>
      </section>

      <section className="lumi-discovery" id="new-arrivals">
        <div className="discovery-glow" />
        <div><span className="lumi-orb"><i /></span><small>{t('discovery.eyebrow')}</small><h2>{t('discovery.title')}</h2><p>{t('discovery.body')}</p></div>
        <div className="discovery-prompts">
          <button onClick={() => askLumi(t('discovery.gift').replaceAll('“', '').replaceAll('”', ''))}>{t('discovery.gift')} <ArrowRight /></button>
          <button onClick={() => askLumi(t('discovery.office').replaceAll('“', '').replaceAll('”', ''))}>{t('discovery.office')} <ArrowRight /></button>
          <button onClick={() => askLumi(t('discovery.battery').replaceAll('“', '').replaceAll('”', ''))}>{t('discovery.battery')} <ArrowRight /></button>
        </div>
        <button className="btn btn-coral" onClick={() => askLumi()}>{t('discovery.cta')} <Sparkles /></button>
      </section>

      <section className="products-section" id="products">
        <div className="products-heading"><div><span>{t('products.eyebrow')}</span><h2>{search ? t('products.search', { search }) : category === 'All' ? t('products.favorites') : t(`category.${category}`)}</h2><p>{t('products.body', { count: visible.length })}</p></div><div className="filter-tabs">{categories.slice(0, 4).map((item) => <button className={category === item ? 'active' : ''} onClick={() => setCategory(item)} key={item}>{t(`category.${item}`)}</button>)}</div></div>
        {visible.length ? <div className="product-grid">{visible.map((product) => <ProductCard key={product.id} product={product} onAdd={addProduct} onView={setSelected} />)}</div> : <div className="no-results"><Sparkles /><h3>{t('products.none')}</h3><p>{t('products.noneBody')}</p><button className="btn btn-primary" onClick={() => { setSearch(''); askLumi() }}>{t('products.ask')}</button></div>}
      </section>

      <section className="editorial" id="offers">
        <article className="editorial-main"><span>{t('editorial.eyebrow')}</span><h2>{t('editorial.title1')}<br />{t('editorial.title2')}</h2><p>{t('editorial.body')}</p><button onClick={() => setSelected(localizedProducts[0])}>{t('editorial.cta')} <ArrowRight /></button></article>
        <article className="editorial-side"><div><small>{t('editorial.smart')}</small><h3>{t('editorial.smartTitle')}</h3></div><button onClick={() => { setCategory('Smart home'); document.querySelector('#products')?.scrollIntoView({ behavior: 'smooth' }) }}>{t('editorial.explore')} <ArrowRight /></button></article>
      </section>

      <section className="benefits" id="benefits">
        <div><span><Truck /></span><b>{t('benefits.shipping')}</b><p>{t('benefits.shippingBody')}</p></div>
        <div><span><RotateCcw /></span><b>{t('benefits.returns')}</b><p>{t('benefits.returnsBody')}</p></div>
        <div><span><ShieldCheck /></span><b>{t('benefits.protected')}</b><p>{t('benefits.protectedBody')}</p></div>
        <div><span><Headphones /></span><b>{t('benefits.support')}</b><p>{t('benefits.supportBody')}</p></div>
      </section>
    </main>
    <footer><div className="footer-brand"><span className="brand"><img className="brand-logo" src="/assets/brand/lumina-logo.png" alt="" /><b>LUMINA</b></span><p>{t('footer.tagline')}</p></div><div><b>{t('footer.discover')}</b><a href="#products">{t('nav.products')}</a><a href="#collections">{t('nav.collections')}</a><a href="#offers">{t('nav.offers')}</a></div><div><b>{t('footer.help')}</b><button onClick={() => askLumi()}>{t('footer.shipping')}</button><button onClick={() => askLumi()}>{t('footer.returns')}</button><button onClick={() => askLumi()}>{t('footer.warranty')}</button></div><div><b>{t('footer.about')}</b><a href="#top">{t('footer.curation')}</a><a href="#top">{t('footer.privacy')}</a><a href="#top">{t('footer.careers')}</a></div><small>{t('footer.legal')}</small></footer>

    <CartDrawer open={cartOpen} items={cart.items} subtotal={cart.subtotal} onClose={() => setCartOpen(false)} onRemove={cart.remove} onUpdate={cart.update} onCheckout={startCheckout} />
    <CheckoutFlow open={checkoutOpen} items={cart.items} subtotal={cart.subtotal} onClose={() => setCheckoutOpen(false)} onSuccess={cart.clear} />
    <ProductModal product={selected} onClose={() => setSelected(null)} onAdd={addProduct} onAsk={askLumi} />
    <Assistant open={assistantOpen} onOpen={() => setAssistantOpen(true)} onClose={() => setAssistantOpen(false)} initialPrompt={assistantPrompt} cart={cart.items} products={products} onViewProduct={setSelected} onOpenCart={() => setCartOpen(true)} />
    {toast && <div className="toast"><span><ShieldCheck /></span>{toast}<button onClick={() => setCartOpen(true)}>{t('toast.viewCart')}</button></div>}
  </div>
}
