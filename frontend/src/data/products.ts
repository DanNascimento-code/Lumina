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
  {
    id: 'aero-earbuds', slug: 'aero-earbuds', name: 'Aero Buds Pro',
    short_description: 'Immersive sound that travels light.',
    description: 'Compact wireless earbuds with adaptive noise cancellation, multipoint pairing and a pocket-sized charging case.',
    category: 'Audio', price: 699.9, old_price: 799.9, rating: 4.8, review_count: 214, stock: 41,
    image_url: '/assets/products/aero-earbuds.jpg', accent: '#ffb178', badges: ['new', '-13%'],
    specs: { Battery: '30h with case', Protection: 'IP54', Connection: 'Bluetooth 5.4' },
  },
  {
    id: 'vector-mouse', slug: 'vector-mouse', name: 'Vector Mouse S',
    short_description: 'Precision shaped for long workdays.',
    description: 'Ergonomic wireless mouse with a quiet magnetic wheel, programmable controls and seamless switching between three devices.',
    category: 'Workspace', price: 429.9, rating: 4.8, review_count: 176, stock: 29,
    image_url: '/assets/products/vector-mouse.jpg', accent: '#91b9ff', badges: ['teamPick'],
    specs: { Battery: '90 days', Sensor: '8000 DPI', Devices: '3 paired' },
  },
  {
    id: 'sentinel-camera', slug: 'sentinel-camera', name: 'Sentinel Cam 2K',
    short_description: 'A clearer view, with privacy built in.',
    description: 'Indoor 2K security camera with person detection, a physical privacy shutter and encrypted local or cloud recording.',
    category: 'Smart home', price: 549.9, rating: 4.7, review_count: 138, stock: 34,
    image_url: '/assets/products/sentinel-camera.jpg', accent: '#8ee0cf', badges: ['smartHome'],
    specs: { Resolution: '2K HDR', 'Field of view': '135°', Connection: 'Dual-band Wi-Fi' },
  },
  {
    id: 'prism-phone', slug: 'prism-phone', name: 'Prism Phone X',
    short_description: 'Flagship speed without the visual noise.',
    description: '5G smartphone with a 120 Hz OLED display, stabilized dual camera and all-day battery in a refined aluminum body.',
    category: 'Mobile', price: 2699.9, old_price: 2999.9, rating: 4.8, review_count: 302, stock: 16,
    image_url: '/assets/products/prism-phone.jpg', accent: '#b39cff', badges: ['new', '-10%'],
    specs: { Storage: '256 GB', Display: '6.4-inch OLED 120 Hz', Battery: '4800 mAh' },
  },
  {
    id: 'slate-tablet', slug: 'slate-tablet', name: 'Slate Tab 11',
    short_description: 'A flexible canvas for work and play.',
    description: 'Thin 11-inch tablet with a 2.5K display, quad speakers, desktop mode and optional pressure-sensitive pen support.',
    category: 'Mobile', price: 2199.9, rating: 4.7, review_count: 167, stock: 23,
    image_url: '/assets/products/slate-tablet.jpg', accent: '#7fd4e7', badges: ['freeShipping'],
    specs: { Storage: '128 GB', Display: '11-inch 2.5K', Battery: 'Up to 12h' },
  },
  {
    id: 'vertex-controller', slug: 'vertex-controller', name: 'Vertex Controller',
    short_description: 'Console feel across every screen.',
    description: 'Low-latency wireless controller with Hall-effect sticks, adjustable triggers and profiles for PC, mobile and cloud gaming.',
    category: 'Gaming', price: 459.9, rating: 4.9, review_count: 189, stock: 38,
    image_url: '/assets/products/vertex-controller.jpg', accent: '#ff9a73', badges: ['bestSeller'],
    specs: { Battery: '30h', Compatibility: 'PC + Android + iOS', Connection: '2.4 GHz + Bluetooth' },
  },
]

export const categories = ['All', 'Audio', 'Wearables', 'Smart home', 'Workspace', 'Accessories', 'Mobile', 'Gaming']

const localizedCopy: Partial<Record<Locale, Record<string, Pick<Product, 'short_description' | 'description' | 'specs'>>>> = {
  'pt-BR': {
    'aurora-headphones': { short_description: 'Silêncio inteligente. Som que abraça.', description: 'Headphone premium com cancelamento adaptativo, áudio espacial e 42 horas de bateria.', specs: { Bateria: '42h', Conexão: 'Bluetooth 5.3', Peso: '268g' } },
    'nimbus-speaker': { short_description: 'Som 360º em qualquer cenário.', description: 'Caixa de som portátil resistente à água com som espacial e pareamento estéreo.', specs: { Bateria: '18h', Proteção: 'IP67', Potência: '40W' } },
    'orbit-watch': { short_description: 'Seu ritmo, traduzido em clareza.', description: 'Smartwatch de titânio com GPS dual-band, métricas de bem-estar e tela AMOLED.', specs: { Bateria: '7 dias', Tela: 'AMOLED 1,43"', Proteção: '5 ATM' } },
    'halo-lamp': { short_description: 'A luz certa para cada momento.', description: 'Luminária inteligente portátil com 16 milhões de cores e automações por rotina.', specs: { Bateria: '10h', Conexão: 'Wi-Fi + Matter', Fluxo: '350 lm' } },
    'flow-keyboard': { short_description: 'Precisão tátil, presença mínima.', description: 'Teclado mecânico low-profile sem fio, hot-swappable e feito para três dispositivos.', specs: { Bateria: '120h', Switch: 'Lumina Linear', Layout: 'ABNT2' } },
    'arc-charger': { short_description: 'Uma base. Três dispositivos. Zero ruído.', description: 'Estação magnética dobrável para celular, relógio e fones, com carregamento de até 15W.', specs: { Potência: '15W', Dispositivos: '3 simultâneos', Cabo: 'USB-C 1,5m' } },
    'aero-earbuds': { short_description: 'Som imersivo que cabe no bolso.', description: 'Fones compactos com cancelamento adaptativo, conexão multiponto e estojo de carregamento.', specs: { Bateria: '30h com estojo', Proteção: 'IP54', Conexão: 'Bluetooth 5.4' } },
    'vector-mouse': { short_description: 'Precisão para jornadas mais confortáveis.', description: 'Mouse sem fio ergonômico com roda magnética silenciosa, controles programáveis e conexão com três dispositivos.', specs: { Bateria: '90 dias', Sensor: '8000 DPI', Dispositivos: '3 pareados' } },
    'sentinel-camera': { short_description: 'Visão mais clara, com privacidade real.', description: 'Câmera interna 2K com detecção de pessoas, obturador físico e gravação local ou em nuvem criptografada.', specs: { Resolução: '2K HDR', Campo: '135°', Conexão: 'Wi-Fi dual-band' } },
    'prism-phone': { short_description: 'Velocidade premium sem excesso visual.', description: 'Smartphone 5G com tela OLED de 120 Hz, câmera dupla estabilizada e bateria para o dia todo.', specs: { Armazenamento: '256 GB', Tela: 'OLED 6,4” 120 Hz', Bateria: '4800 mAh' } },
    'slate-tablet': { short_description: 'Uma tela flexível para criar e relaxar.', description: 'Tablet fino de 11 polegadas com tela 2.5K, quatro alto-falantes e modo desktop.', specs: { Armazenamento: '128 GB', Tela: '11” 2.5K', Bateria: 'Até 12h' } },
    'vertex-controller': { short_description: 'Experiência de console em qualquer tela.', description: 'Controle sem fio de baixa latência com analógicos Hall, gatilhos ajustáveis e perfis para PC e mobile.', specs: { Bateria: '30h', Compatibilidade: 'PC + Android + iOS', Conexão: '2,4 GHz + Bluetooth' } },
  },
  'es-419': {
    'aurora-headphones': { short_description: 'Silencio inteligente. Sonido envolvente.', description: 'Audífonos premium con cancelación adaptativa, audio espacial y 42 horas de batería.', specs: { Batería: '42h', Conexión: 'Bluetooth 5.3', Peso: '268g' } },
    'nimbus-speaker': { short_description: 'Sonido 360° en cualquier lugar.', description: 'Altavoz portátil resistente al agua con sonido espacial y emparejamiento estéreo.', specs: { Batería: '18h', Protección: 'IP67', Potencia: '40W' } },
    'orbit-watch': { short_description: 'Tu ritmo, traducido en claridad.', description: 'Smartwatch de titanio con GPS de doble banda, métricas de bienestar y pantalla AMOLED.', specs: { Batería: '7 días', Pantalla: 'AMOLED 1,43"', Protección: '5 ATM' } },
    'halo-lamp': { short_description: 'La luz adecuada para cada momento.', description: 'Lámpara inteligente portátil con 16 millones de colores y automatizaciones.', specs: { Batería: '10h', Conexión: 'Wi-Fi + Matter', Flujo: '350 lm' } },
    'flow-keyboard': { short_description: 'Precisión táctil, presencia mínima.', description: 'Teclado mecánico inalámbrico de perfil bajo, hot-swappable y para tres dispositivos.', specs: { Batería: '120h', Switch: 'Lumina Linear', Diseño: 'ABNT2' } },
    'arc-charger': { short_description: 'Una base. Tres dispositivos. Sin desorden.', description: 'Estación magnética plegable para teléfono, reloj y audífonos con carga de hasta 15W.', specs: { Potencia: '15W', Dispositivos: '3 simultáneos', Cable: 'USB-C 1,5m' } },
    'aero-earbuds': { short_description: 'Sonido inmersivo que cabe en tu bolsillo.', description: 'Audífonos compactos con cancelación adaptativa, conexión multipunto y estuche de carga.', specs: { Batería: '30h con estuche', Protección: 'IP54', Conexión: 'Bluetooth 5.4' } },
    'vector-mouse': { short_description: 'Precisión para jornadas más cómodas.', description: 'Mouse inalámbrico ergonómico con rueda magnética silenciosa, controles programables y tres dispositivos.', specs: { Batería: '90 días', Sensor: '8000 DPI', Dispositivos: '3 vinculados' } },
    'sentinel-camera': { short_description: 'Una visión más clara con privacidad real.', description: 'Cámara interior 2K con detección de personas, obturador físico y grabación local o cifrada en la nube.', specs: { Resolución: '2K HDR', Campo: '135°', Conexión: 'Wi-Fi doble banda' } },
    'prism-phone': { short_description: 'Velocidad premium sin ruido visual.', description: 'Smartphone 5G con pantalla OLED de 120 Hz, cámara doble estabilizada y batería para todo el día.', specs: { Almacenamiento: '256 GB', Pantalla: 'OLED 6,4” 120 Hz', Batería: '4800 mAh' } },
    'slate-tablet': { short_description: 'Un lienzo flexible para crear y disfrutar.', description: 'Tablet delgada de 11 pulgadas con pantalla 2.5K, cuatro altavoces y modo escritorio.', specs: { Almacenamiento: '128 GB', Pantalla: '11” 2.5K', Batería: 'Hasta 12h' } },
    'vertex-controller': { short_description: 'Sensación de consola en cualquier pantalla.', description: 'Control inalámbrico de baja latencia con sticks Hall, gatillos ajustables y perfiles para PC y móvil.', specs: { Batería: '30h', Compatibilidad: 'PC + Android + iOS', Conexión: '2,4 GHz + Bluetooth' } },
  },
}

export function localizeProduct(product: Product, locale: Locale): Product {
  return { ...product, ...(localizedCopy[locale]?.[product.id] ?? {}) }
}
