import React, { useState } from 'react';
import { 
  StyleSheet, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  View, 
  ActivityIndicator, 
  ScrollView,
  Keyboard
} from 'react-native';
import axios from 'axios';

// URL DO SEU BACKEND EM FLASK (JÁ COM O SEU IP LOCAL CONFIGURADO)
const API_URL = 'http://192.168.1.103:5000/analisar';

export default function App() {
  const [texto, setTexto] = useState('');
  const [resultado, setResultado] = useState(null);
  const [carregando, setCarregando] = useState(false);

  const verificarNoticia = async () => {
    if (!texto.trim()) {
      alert('Por favor, digite ou cole uma afirmação antes de verificar.');
      return;
    }

    Keyboard.dismiss(); 
    setCarregando(true);
    setResultado(null);

    try {
      // Dispara a requisição para o Flask passando a notícia no corpo do JSON
      const resposta = await axios.post(API_URL, { texto: texto });
      setResultado(resposta.data);
    } catch (error) {
      console.log(error);
      alert('Erro ao conectar com o servidor. Verifique se o seu celular e o PC estão na mesma rede Wi-Fi.');
    } finally {
      setCarregando(false);
    }
  };

  // Define a cor do card com base no resultado da análise
  const obterCorResultado = (status) => {
    if (!status) return '#718096';
    const termo = status.toLowerCase();
    if (termo.includes('falso') || termo.includes('fake')) return '#E53E3E'; // Vermelho para fakes[cite: 1]
    if (termo.includes('verdade') || termo.includes('true')) return '#38A169'; // Verde para reais[cite: 1]
    return '#DD6B20'; // Laranja para outros casos[cite: 1]
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.titulo}>Detector IA de Fake News</Text>
      <Text style={styles.subtitulo}>Atividade Orientada de Trabalho (OAT)</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Cole ou digite aqui a afirmação ou notícia que deseja analisar..."
        placeholderTextColor="#A0AEC0"
        multiline
        numberOfLines={5}
        value={texto}
        onChangeText={setTexto}
      />

      <TouchableOpacity 
        style={styles.botao} 
        onPress={verificarNoticia}
        disabled={carregando}
      >
        {carregando ? (
          <ActivityIndicator color="#FFF" />
        ) : (
          <Text style={styles.textoBotao}>Verificar Notícia</Text>
        )}
      </TouchableOpacity>

      {resultado && (
        <View style={[styles.cardResultado, { backgroundColor: obterCorResultado(resultado.resultado) }]}>
          <Text style={styles.resultadoTitulo}>Análise Concluída</Text>
          <Text style={styles.resultadoTexto}>
            <Text style={{ fontWeight: 'bold' }}>Resultado: </Text>
            {resultado.resultado}
          </Text>
          <Text style={styles.resultadoMeta}>
            <Text style={{ fontWeight: 'bold' }}>Origem: </Text>
            {resultado.origem}
          </Text>
          <Text style={styles.resultadoDetalhe}>{resultado.detalhe}</Text>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#1A202C',
    alignItems: 'center',
    padding: 20,
    paddingTop: 60,
  },
  titulo: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFF',
    marginBottom: 5,
    textAlign: 'center'
  },
  subtitulo: {
    fontSize: 14,
    color: '#CBD5E0',
    marginBottom: 30,
    textAlign: 'center'
  },
  input: {
    width: '100%',
    backgroundColor: '#2D3748',
    color: '#FFF',
    borderRadius: 10,
    padding: 15,
    fontSize: 16,
    textAlignVertical: 'top',
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#4A5568'
  },
  botao: {
    width: '100%',
    backgroundColor: '#3182CE',
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 25,
    elevation: 2,
  },
  textoBotao: {
    color: '#FFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  cardResultado: {
    width: '100%',
    borderRadius: 10,
    padding: 20,
    marginTop: 10,
    elevation: 5,
  },
  resultadoTitulo: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFF',
    marginBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(255,255,255,0.3)',
    paddingBottom: 5
  },
  resultadoTexto: {
    fontSize: 16,
    color: '#FFF',
    marginBottom: 8
  },
  resultadoMeta: {
    fontSize: 14,
    color: '#FFF',
    opacity: 0.9,
    marginBottom: 8
  },
  resultadoDetalhe: {
    fontSize: 13,
    color: '#FFF',
    fontStyle: 'italic',
    marginTop: 5,
    backgroundColor: 'rgba(0,0,0,0.15)',
    padding: 8,
    borderRadius: 5
  }
});