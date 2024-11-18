# -*- coding: utf-8 -*-
"""calculadora

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yitM6A7QKbErCzxP1Zl38MNl0ciCjSzw
"""

import streamlit as st
import numpy as np
import scipy.stats as si

# Black-Scholes Function
def black_scholes(S, K, r, T, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        price = S * si.norm.cdf(d1) - K * np.exp(-r * T) * si.norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * si.norm.cdf(-d2) - S * si.norm.cdf(-d1)
    return price

# Asian Option Function (Monte Carlo)
def asian_option(S, K, r, T, sigma, n_simulations, n_steps, option_type="call"):
    dt = T / n_steps
    discount_factor = np.exp(-r * T)
    prices = np.zeros((n_simulations, n_steps + 1))
    prices[:, 0] = S
    for t in range(1, n_steps + 1):
        z = np.random.standard_normal(n_simulations)
        prices[:, t] = prices[:, t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)
    mean_prices = np.mean(prices[:, 1:], axis=1)
    if option_type == "call":
        payoffs = np.maximum(mean_prices - K, 0)
    elif option_type == "put":
        payoffs = np.maximum(K - mean_prices, 0)
    return discount_factor * np.mean(payoffs)

# Binary Option Function
def binary_option(S, K, r, T, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == "call":
        price = np.exp(-r * T) * si.norm.cdf(d2)
    elif option_type == "put":
        price = np.exp(-r * T) * si.norm.cdf(-d2)
    return price

# Streamlit App
def main():
    st.title("Calculadora de Opções")
    st.sidebar.title("Configurações")

    # Escolher o tipo de opção
    option_type = st.sidebar.selectbox("Escolha o Tipo de Opção", ("Black-Scholes", "Asiática", "Binária"))
    call_put = st.sidebar.selectbox("Tipo de Opção", ("Call", "Put"))

    # Parâmetros comuns
    S = st.sidebar.number_input("Preço da Ação (S)", value=100.0)
    K = st.sidebar.number_input("Preço de Exercício (K)", value=100.0)
    r = st.sidebar.number_input("Taxa Livre de Risco (r)", value=0.05)
    T = st.sidebar.number_input("Tempo até o Vencimento (T) em anos", value=1.0)
    sigma = st.sidebar.number_input("Volatilidade (σ)", value=0.2)

    if option_type == "Asiática":
        n_simulations = st.sidebar.number_input("Número de Simulações", value=10000, step=1000)
        n_steps = st.sidebar.number_input("Passos de Tempo", value=252, step=1)

    # Botão de cálculo
    if st.sidebar.button("Calcular"):
        if option_type == "Black-Scholes":
            price = black_scholes(S, K, r, T, sigma, call_put.lower())
            st.success(f"O preço da opção {option_type} ({call_put}) é: R${price:.2f}")

        elif option_type == "Asiática":
            price = asian_option(S, K, r, T, sigma, int(n_simulations), int(n_steps), call_put.lower())
            st.success(f"O preço da opção {option_type} ({call_put}) é: R${price:.2f}")

        elif option_type == "Binária":
            price = binary_option(S, K, r, T, sigma, call_put.lower())
            st.success(f"O preço da opção {option_type} ({call_put}) é: R${price:.2f}")

if __name__ == "__main__":
    main()