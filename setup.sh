mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"221810402010@gitam.in\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
\n\
" > ~/.streamlit/config.toml
