// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    app: {
        head: {
        title: 'UKKW SIWP2005 Final Project',
            htmlAttrs: {
                lang: 'en'
            },
            link: [
                { rel: 'SHORTCUT ICON', type: 'image/png', href: '/favicon.png' }
            ],
            meta: [
                { charset: 'utf-8' },
                { name: 'viewport', content: 'width=device-width, initial-scale=1' },
                { hid: 'description', name: 'description', content: '' },
                { name: 'format-detection', content: 'telephone=no' }
            ],
        },
    },
    modules: [
        '@invictus.codes/nuxt-vuetify',
        '@sidebase/nuxt-auth',
    ],
    
    ssr: true,
    css: [
        'vuetify/lib/styles/main.sass',
        '@mdi/font/css/materialdesignicons.min.css',
    ],
    build: {
        transpile: ['vuetify'], 
    },

    vite: {
        define: {
            'process.env.DEBUG': false,
        },
    },
    auth: {
        provider: {
            type: 'local',
            pages: {
                login: '/'
            },
        },
        globalAppMiddleware: {
            isEnabled: true,
        },

    },
    devServer: {
        host: '0.0.0.0',
        port: 3000,
    },
    runtimeConfig: {
        api: {
            authUrl: process.env.API_AUTH,
        },
        public: {
            API_BASE: process.env.API_BASE,
        },
    }
})
