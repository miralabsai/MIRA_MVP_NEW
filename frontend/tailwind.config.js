/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  mode: "jit",
  theme: {
    extend: {
      colors: {
        'primary': '#00040f',
        'secondary': '#00f6ff',
        'dimWhite': 'rgba(255, 255, 255, 0.7)',
        'dimBlue': 'rgba(9, 151, 124, 0.1)',
        'poppy': '#d64045',
        'mint-green': '#e9fff9',
        'non-photo-blue': '#9ed8db',
        'ucla-blue': '#467599',
        'delft-blue': '#1d3354',
      },
      backgroundImage: theme => ({
        'gradient-top': 'linear-gradient(0deg, #d64045, #e9fff9, #9ed8db, #467599, #1d3354)',
        'gradient-right': 'linear-gradient(90deg, #d64045, #e9fff9, #9ed8db, #467599, #1d3354)',
        'gradient-bottom': 'linear-gradient(180deg, #d64045, #e9fff9, #9ed8db, #467599, #1d3354)',
        'gradient-left': 'linear-gradient(270deg, #d64045, #e9fff9, #9ed8db, #467599, #1d3354)',
        'gradient-top-right': 'linear-gradient(45deg, #d64045, #e9fff9, #9ed8db, #467599, #1d3354)',
        'gradient-bottom-right': 'linear-gradient(135deg, #d64045, #e9fff9, #9ed8db, #467599, #1d3354)',
        'gradient-top-left': 'linear-gradient(225deg, #d64045, #e9fff9, #9ed8db, #467599, #1d3354)',
        'gradient-bottom-left': 'linear-gradient(315deg, #d64045, #e9fff9, #9ed8db, #467599, #1d3354)',
        'gradient-radial': 'radial-gradient(#d64045, #e9fff9, #9ed8db, #467599, #1d3354)',
      }),
      variants: {
        extend: {
          backgroundColor: ['active', 'focus', 'hover', 'group-hover'], // Added 'focus', 'hover', 'group-hover'
          borderColor: ['focus', 'focus-within'], // Added 'focus-within'
          textColor: ['visited', 'hover'], // Added 'visited', 'hover'
          opacity: ['disabled'], // Added 'disabled'
        },
      },
      fontFamily: {
        'Oxygen': ['Oxygen', 'sans-serif'],
      },
      
    },
    screens: {
      xs: "480px",
      ss: "620px",
      sm: "768px",
      md: "1060px",
      lg: "1200px",
      xl: "1700px",
    },
  },
  plugins: [],
};