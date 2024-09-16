import streamlit as st


def mkd_text_divider(text: str, level: str = 'title', position: str = 'center'):
    """
    Função para escrever títulos, headers e subheaders centralizados ou não.

    Parâmetros:
    text (str): O texto a ser exibido.
    level (str): Nível do texto ('title', 'header', 'subheader').
    position (str): Posição do texto ('center' para centralizado, 'left' para à esquerda).
    """
    # Pegar a cor selecionada dinamicamente do session_state
    text_color = st.session_state.get("text_color", "#000000")  # Padrão preto se não definido
    col = st.columns([0.3, 0.4, 0.3])
    with col[0]:
        st.divider()
    with col[1]:
        if position == 'center':
            html_tag = {
                'title': 'h1',
                'header': 'h2',
                'subheader': 'h3',
                'h4': 'h4',
                'h5': 'h5',
                'h6': 'h6',
                'h7': 'h7',
            }.get(level, 'h1')  # Usa 'h1' como padrão se o nível não for reconhecido
            st.markdown(
                f"<{html_tag} style='text-align: center; color: {text_color};'>{text}</{html_tag}>", 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<{html_tag} style='text-align: left; color: {text_color};'>{text}</{html_tag}>", 
                unsafe_allow_html=True
            )
        with col[2]:
            st.divider()


def mkd_text(text: str, level: str = 'title', position: str = 'center'):
    """
    Função para escrever títulos, headers e subheaders centralizados ou não.

    Parâmetros:
    text (str): O texto a ser exibido.
    level (str): Nível do texto ('title', 'header', 'subheader').
    position (str): Posição do texto ('center' para centralizado, 'left' para à esquerda).
    """
    # Pegar a cor selecionada dinamicamente do session_state
    text_color = st.session_state.get("text_color", "#000000")  # Padrão preto se não definido

    if position == 'center':
        html_tag = {
            'title': 'h1',
            'header': 'h2',
            'subheader': 'h3',
            'h4': 'h4',
            'h5': 'h5',
            'h6': 'h6',
            'h7': 'h7',
        }.get(level, 'h1')  # Usa 'h1' como padrão se o nível não for reconhecido
        st.markdown(
            f"<{html_tag} style='text-align: center; color: {text_color};'>{text}</{html_tag}>", 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<{html_tag} style='text-align: left; color: {text_color};'>{text}</{html_tag}>", 
            unsafe_allow_html=True
        )


def mkd_paragraph(text: str, position: str = 'justify'):
    """
    Função para escrever parágrafos centralizados ou não.

    Parâmetros:
    text (str): O texto a ser exibido.
    position (str): Posição do texto ('center' para centralizado, 'left' para à esquerda).
    """
    if position == 'center':
        st.markdown(f"<p style='text-align: center;'>{text}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='text-align: justify;'>{text}</p>", unsafe_allow_html=True)