import { View, Text, StyleSheet, Pressable } from 'react-native'
import React from 'react'

const CustomButtonStarted = ({onPress, text}) => {
  return (
    <Pressable onPress={onPress} style={styles.container}>
      <Text style={styles.text}>{text}</Text>
    </Pressable>
  )
}

const styles= StyleSheet.create({
    container:{
        backgroundColor: '#7a1628',
        width: '80%',
        height: 60,
        padding: 16,
        alignItems: 'center',
        borderRadius: 5,
        top: 748,
        position: 'absolute',
    },
    text:{
        fontWeight: 'bold',
        color: 'white',
    },

});
export default CustomButtonStarted