<template>
    <div id="letter-container" :style="{ transitionDelay: `${0.15 + 0.3 * (placement - 1)}s`, animationDelay: `${0.3 * (placement - 1)}s` }" :class="{ 
        validated: color, 
        correct: color === 'correct', 
        partial: color === 'partial', 
        incorrect: color === 'incorrect',
        partialmei: color === 'partialmei', 
        'no-animation': !animate,
        'color-blind': colorBlindMode,
    }">
        <div class="letter" v-if="letter" :style="{ transitionDelay: `${0.15 + 0.3 * (placement - 1)}s`}">
            {{ letter }}
        </div>
    </div>
</template>

<script>

export default {
    name: 'LetterContainer',
    props: {
        letter: String,
        placement: Number,
        color: String,
        animate: Boolean,
        colorBlindMode: Boolean,
    },
}
</script>

<style lang="sass" scoped>
#letter-container
    width: 64px
    height: 64px
    border: 2px solid #919191
    box-sizing: border-box
    margin: 2px
    transition: transform 0.1s, background 0.1s, border 0.1s
    @media (max-width: 380px)
        width: 54px
        height: 54px
        @media (max-width: 300px)
            width: 48px
            height: 48px
    @media (max-height: 600px)
        width: 48px
        height: 48px
        @media (max-height: 480px)
            width: 40px
            height: 40px
    &.validated
        animation: flip
        animation-duration: 0.5s
        animation-timing-function: ease-in-out
        animation-fill-mode: forwards
        .letter
            transition: all 0.1s
            transform: rotateX(180deg)
        &.color-blind
            .letter
                color: white
    &.correct
        border: 2px solid #538D4E
        background: #538D4E
        animation-name: flip
        &.color-blind
            border: 2px solid #F5793A
            background: #F5793A
    &.partial
        border: 2px solid #B59E3B
        background: #B59E3B
        animation-name: flip
        &.color-blind
            border: 2px solid #85C0F9
            background: #85C0F9
    &.incorrect
        border: 2px solid #3A3A3C
        background: #3A3A3C
    &.partialmei
        border: 2px solid #957D95
        background: #957D95
        animation-name: flip
        &.color-blind
            border: 2px solid #D81E5B
            background: #D81E5B
    &.no-animation
        transition: none
        animation: none
        transform: none
        .letter
            transition: none
            transform: none
    .letter
        width: 100%
        height: 100%
        color: #D1DFD4
        display: flex
        align-items: center
        justify-content: center
        font-weight: bolder
        font-size: 36px
        position: relative
        z-index: 3
        @media (max-height: 480px)
            font-size: 28px

    @keyframes flip
        from
            transform: rotateX(0deg)
        to
            transform: rotateX(180deg)
</style>