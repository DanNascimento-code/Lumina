import type { Product } from '../types'
import type { Locale } from '../i18n'

export const products: Product[] = [
  {
    id: 'aurora-headphones', slug: 'aurora-headphones', name: 'Aurora Headphones',
    short_description: 'Intelligent silence. Sound that surrounds you.',
    description: 'Premium headphones with adaptive noise cancellation, spatial audio and 42 hours of battery life.',
    category: 'Audio', price: 1299.9, old_price: 1499.9, rating: 4.9, review_count: 328, stock: 18,
    image_url: '/assets/products/aurora-headphones.jpg',
    accent: '#f68b70', badges: ['bestSeller', '-13%'],
    specs: { Battery: '42h', Connection: 'Bluetooth 5.3', Weight: '268g' },
  },
  {
    id: 'nimbus-speaker', slug: 'nimbus-speaker', name: 'Nimbus Speaker',
    short_description: 'Room-filling 360° sound, wherever you go.',
    description: 'Water-resistant portable speaker with spatial sound and stereo pairing.',
    category: 'Audio', price: 749.9, rating: 4.8, review_count: 196, stock: 32,
    image_url: '/assets/products/nimbus-speaker.jpg',
    accent: '#ad8cff', badges: ['freeShipping'],
    specs: { Battery: '18h', Protection: 'IP67', Power: '40W' },
  },
  {
    id: 'orbit-watch', slug: 'orbit-watch', name: 'Orbit Watch S2',
    short_description: 'Your rhythm, translated into clarity.',
    description: 'Titanium smartwatch with dual-band GPS, wellness insights and an AMOLED display.',
    category: 'Wearables', price: 1599.9, old_price: 1799.9, rating: 4.9, review_count: 241, stock: 14,
    image_url: '/assets/products/orbit-watch.jpg',
    accent: '#83d9c8', badges: ['new', '-11%'],
    specs: { Battery: '7 days', Display: '1.43" AMOLED', Protection: '5 ATM' },
  },
  {
    id: 'halo-lamp', slug: 'halo-lamp', name: 'Halo Light Mini',
    short_description: 'The right light for every moment.',
    description: 'Portable smart lamp with 16 million colors and routine-based automations.',
    category: 'Smart home', price: 389.9, rating: 4.7, review_count: 154, stock: 46,
    image_url: '/assets/products/halo-lamp.jpg',
    accent: '#ffd082', badges: ['smartHome'],
    specs: { Battery: '10h', Connection: 'Wi-Fi + Matter', Output: '350 lm' },
  },
  {
    id: 'flow-keyboard', slug: 'flow-keyboard', name: 'Flow Keys Pro',
    short_description: 'Tactile precision, minimal presence.',
    description: 'Wireless low-profile mechanical keyboard, hot-swappable and built for three devices.',
    category: 'Workspace', price: 899.9, rating: 4.8, review_count: 112, stock: 21,
    image_url: '/assets/products/flow-keyboard.jpg',
    accent: '#7ea8ff', badges: ['teamPick'],
    specs: { Battery: '120h', Switch: 'Lumina Linear', Layout: 'ABNT2' },
  },
  {
    id: 'arc-charger', slug: 'arc-charger', name: 'Arc Charger 3-in-1',
    short_description: 'One base. Three devices. Zero clutter.',
    description: 'Foldable magnetic station for phone, watch and earbuds with charging up to 15W.',
    category: 'Accessories', price: 499.9, old_price: 579.9, rating: 4.7, review_count: 89, stock: 37,
    image_url: '/assets/products/arc-charger.jpg',
    accent: '#ff9db4', badges: ['-14%'],
    specs: { Power: '15W', Devices: '3 at once', Cable: '1.5m USB-C' },
  },
]

export const categories = ['All', 'Audio', 'Wearables', 'Smart home', 'Workspace', 'Accessories']

const localizedCopy: Partial<Record<Locale, Record<string, Pick<Product, 'short_description' | 'description' | 'specs'>>>> = {
  'pt-BR': {
    'aurora-headphones': { short_description: 'Silêncio inteligente. Som que abraça.', description: 'Headphone premium com cancelamento adaptativo, áudio espacial e 42 horas de bateria.', specs: { Bateria: '42h', Conexão: 'Bluetooth 5.3', Peso: '268g' } },
    'nimbus-speaker': { short_description: 'Som 360º em qualquer cenário.', description: 'Caixa de som portátil resistente à água com som espacial e pareamento estéreo.', specs: { Bateria: '18h', Proteção: 'IP67', Potência: '40W' } },
    'orbit-watch': { short_description: 'Seu ritmo, traduzido em clareza.', description: 'Smartwatch de titânio com GPS dual-band, métricas de bem-estar e tela AMOLED.', specs: { Bateria: '7 dias', Tela: 'AMOLED 1,43"', Proteção: '5 ATM' } },
    'halo-lamp': { short_description: 'A luz certa para cada momento.', description: 'Luminária inteligente portátil com 16 milhões de cores e automações por rotina.', specs: { Bateria: '10h', Conexão: 'Wi-Fi + Matter', Fluxo: '350 lm' } },
    'flow-keyboard': { short_description: 'Precisão tátil, presença mínima.', description: 'Teclado mecânico low-profile sem fio, hot-swappable e feito para três dispositivos.', specs: { Bateria: '120h', Switch: 'Lumina Linear', Layout: 'ABNT2' } },
    'arc-charger': { short_description: 'Uma base. Três dispositivos. Zero ruído.', description: 'Estação magnética dobrável para celular, relógio e fones, com carregamento de até 15W.', specs: { Potência: '15W', Dispositivos: '3 simultâneos', Cabo: 'USB-C 1,5m' } },
  },
  'es-419': {
    'aurora-headphones': { short_description: 'Silencio inteligente. Sonido envolvente.', description: 'Audífonos premium con cancelación adaptativa, audio espacial y 42 horas de batería.', specs: { Batería: '42h', Conexión: 'Bluetooth 5.3', Peso: '268g' } },
    'nimbus-speaker': { short_description: 'Sonido 360° en cualquier lugar.', description: 'Altavoz portátil resistente al agua con sonido espacial y emparejamiento estéreo.', specs: { Batería: '18h', Protección: 'IP67', Potencia: '40W' } },
    'orbit-watch': { short_description: 'Tu ritmo, traducido en claridad.', description: 'Smartwatch de titanio con GPS de doble banda, métricas de bienestar y pantalla AMOLED.', specs: { Batería: '7 días', Pantalla: 'AMOLED 1,43"', Protección: '5 ATM' } },
    'halo-lamp': { short_description: 'La luz adecuada para cada momento.', description: 'Lámpara inteligente portátil con 16 millones de colores y automatizaciones.', specs: { Batería: '10h', Conexión: 'Wi-Fi + Matter', Flujo: '350 lm' } },
    'flow-keyboard': { short_description: 'Precisión táctil, presencia mínima.', description: 'Teclado mecánico inalámbrico de perfil bajo, hot-swappable y para tres dispositivos.', specs: { Batería: '120h', Switch: 'Lumina Linear', Diseño: 'ABNT2' } },
    'arc-charger': { short_description: 'Una base. Tres dispositivos. Sin desorden.', description: 'Estación magnética plegable para teléfono, reloj y audífonos con carga de hasta 15W.', specs: { Potencia: '15W', Dispositivos: '3 simultáneos', Cable: 'USB-C 1,5m' } },
  },
}

export function localizeProduct(product: Product, locale: Locale): Product {
  return { ...product, ...(localizedCopy[locale]?.[product.id] ?? {}) }
}
