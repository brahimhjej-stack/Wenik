import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';

const colors = {
  background: '#09090d',
  surface: '#14141b',
  text: '#ffffff',
  muted: '#aaaab5',
  pink: '#ef159d',
  orange: '#ff7a00',
  yellow: '#ffd43b',
  purple: '#7c3cff'
};

const items = [
  ['WIN', 'Gifts & rewards'],
  ['IZA', 'Vote & participate'],
  ['QR', 'Scan at partners'],
  ['Partners', 'Discover WENIK partners']
];

export default function Home() {
  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.page}>
        <View style={styles.brand}>
          <Text style={styles.logo}>WENIK</Text>
          <Text style={styles.winwin}>WIN WIN</Text>
        </View>

        <View style={styles.hero}>
          <Text style={styles.eyebrow}>WELCOME TO WENIK</Text>
          <Text style={styles.title}>Discover. Save. Win.</Text>
          <Text style={styles.copy}>Your WENIK experience, now built for mobile.</Text>
        </View>

        <View style={styles.grid}>
          {items.map(([title, sub], i) => (
            <View key={title} style={styles.card}>
              <View style={[styles.dot, { backgroundColor: [colors.pink, colors.orange, colors.yellow, colors.purple][i] }]} />
              <Text style={styles.cardTitle}>{title}</Text>
              <Text style={styles.cardSub}>{sub}</Text>
            </View>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.background },
  page: { padding: 20, paddingBottom: 40 },
  brand: { alignItems: 'center', marginTop: 12, marginBottom: 24 },
  logo: { color: colors.text, fontSize: 32, fontWeight: '900', letterSpacing: 3 },
  winwin: { color: colors.pink, fontSize: 12, fontWeight: '800', letterSpacing: 4, marginTop: 3 },
  hero: { backgroundColor: colors.surface, borderRadius: 28, padding: 24, marginBottom: 18 },
  eyebrow: { color: colors.orange, fontSize: 12, fontWeight: '800', letterSpacing: 1.5 },
  title: { color: colors.text, fontSize: 30, fontWeight: '900', marginTop: 8 },
  copy: { color: colors.muted, fontSize: 15, marginTop: 8, lineHeight: 22 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  card: { width: '48%', minHeight: 150, backgroundColor: colors.surface, borderRadius: 22, padding: 18 },
  dot: { width: 12, height: 12, borderRadius: 6, marginBottom: 22 },
  cardTitle: { color: colors.text, fontSize: 20, fontWeight: '900' },
  cardSub: { color: colors.muted, fontSize: 13, marginTop: 7, lineHeight: 18 }
});
