<script setup>
defineProps({ name: { type: String, default: 'daisy' } })
</script>

<template>
  <svg viewBox="0 0 100 100" fill="none" aria-hidden="true" class="plant-art">
    <g v-if="name === 'sprout'" stroke="#326347" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M50 79V46"/><path d="M49 59C27 61 16 48 20 29c20-1 32 10 29 30Z" fill="#99B485"/><path d="M51 49c-1-20 12-31 30-29 1 20-11 31-30 29Z" fill="#5D8E63"/><path d="m31 41 18 18m19-26L51 49"/>
      <path d="M29 82h43" stroke="#CBB58D"/>
    </g>
    <g v-else-if="name === 'tulip'" stroke="#446748" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
      <path d="M50 83V47"/><path d="M50 75C31 73 27 64 26 56c13 0 21 8 24 19Z" fill="#8DA876"/><path d="M50 66c17-1 24-10 25-19-12 0-21 6-25 19Z" fill="#6E9569"/>
      <path d="M50 51C29 50 27 32 30 19l13 9 7-13 9 13 12-9c3 20-3 32-21 32Z" fill="#DA8C81" stroke="#AB625B"/>
      <path d="M43 29c0 9 2 16 7 21m9-22c1 9-3 17-9 22" stroke="#C4776D"/>
    </g>
    <g v-else-if="name === 'daisy'">
      <path d="M50 86V47M50 76c18-1 23-9 25-17-13-1-21 7-25 17Z" stroke="#587F50" stroke-width="3" stroke-linecap="round" fill="#91AC7C"/>
      <g fill="#FBF2D7" stroke="#C7AD7E" stroke-width="1.5">
        <ellipse cx="50" cy="26" rx="8" ry="15"/><ellipse cx="50" cy="58" rx="8" ry="15"/>
        <ellipse cx="34" cy="42" rx="15" ry="8"/><ellipse cx="66" cy="42" rx="15" ry="8"/>
        <ellipse cx="38" cy="30" rx="8" ry="13" transform="rotate(-45 38 30)"/><ellipse cx="62" cy="30" rx="8" ry="13" transform="rotate(45 62 30)"/>
        <ellipse cx="38" cy="54" rx="8" ry="13" transform="rotate(45 38 54)"/><ellipse cx="62" cy="54" rx="8" ry="13" transform="rotate(-45 62 54)"/>
      </g><circle cx="50" cy="42" r="12" fill="#DBAC50"/><circle cx="47" cy="39" r="2" fill="#B98A38"/><circle cx="54" cy="44" r="2" fill="#B98A38"/>
    </g>
    <g v-else-if="name === 'cactus'" stroke="#3B7155" stroke-width="3" stroke-linejoin="round">
      <path d="M42 71V31c0-17 19-17 19 0v19h6V36c0-9 12-9 12 0v17c0 8-9 10-18 10v9H42Z" fill="#82A781"/>
      <path d="M42 58H30c-8 0-11-4-11-11V34c0-8 12-8 12 0v12h11" fill="#82A781"/>
      <path d="M51 29v41M29 75h45l-6 17H35Z" fill="#D6A47B" stroke="#B47C55"/><path d="m39 84 26 0" stroke="#BE895F"/>
      <path d="M52 13c-8-9-2-14 3-8 6-4 10 3-3 8" fill="#DF9B9C" stroke="#C17C87" stroke-width="1.5"/>
    </g>
    <g v-else-if="name === 'leaf'" stroke="#4E7650" stroke-width="3" stroke-linecap="round">
      <path d="M25 76C17 43 43 18 79 18c0 34-16 64-54 58Z" fill="#9FB987"/><path d="m21 84 43-48m-27 29 1-20m8 10 22-1m-15-9 1-17"/>
    </g>
    <g v-else-if="name === 'cherry'" stroke-linecap="round" stroke-linejoin="round">
      <path d="M31 62c8-5 19-25 23-44m12 49c0-24-5-38-12-49" stroke="#55794F" stroke-width="3"/><path d="M54 22c10-14 22-12 29-6-9 12-19 14-29 6Z" fill="#8CAA73" stroke="#55794F" stroke-width="2"/>
      <circle cx="30" cy="69" r="17" fill="#C96661"/><circle cx="67" cy="73" r="17" fill="#B85354"/><path d="M23 61c-3 1-5 4-5 7m42-3c-3 1-5 4-5 7" stroke="#F1B3A2" stroke-width="4"/>
    </g>
    <g v-else-if="name === 'mushroom'" stroke="#986B50" stroke-width="2.5" stroke-linejoin="round">
      <path d="m42 48-5 33c6 8 21 8 28 0l-7-33" fill="#F4E4C7"/><path d="M13 51c6-47 68-48 75 0-19 12-56 12-75 0Z" fill="#C97B62"/>
      <ellipse cx="51" cy="53" rx="37" ry="8" fill="#E7C9A8"/><circle cx="34" cy="33" r="6" fill="#F8E7CB" stroke="none"/><circle cx="58" cy="26" r="5" fill="#F8E7CB" stroke="none"/><circle cx="72" cy="41" r="4" fill="#F8E7CB" stroke="none"/>
    </g>
    <g v-else-if="name === 'orange'" stroke-linecap="round">
      <circle cx="49" cy="59" r="29" fill="#DFA454" stroke="#C68C3E" stroke-width="2.5"/><path d="m50 30 3-14" stroke="#6D7046" stroke-width="4"/><path d="M52 24c4-16 21-17 29-9-5 13-18 18-29 9Z" fill="#72966A" stroke="#517A50" stroke-width="2"/><path d="M31 46c-5 5-6 12-5 17" stroke="#F5CC8B" stroke-width="4"/>
    </g>
    <g v-else-if="name === 'clover'" fill="#8DAB7A" stroke="#507E55" stroke-width="2.5" stroke-linejoin="round">
      <path d="M50 50C22 40 16 27 25 19s24 0 25 13c3-17 19-22 26-13s1 23-26 31Z"/><path d="M50 50c-26 0-38 10-32 23 8 13 23 7 32-9 6 19 25 21 31 8 6-15-10-24-31-22Z"/><path d="M50 49c7 18 4 31-7 42" fill="none" stroke-width="4"/>
    </g>
    <g v-else-if="name === 'sunflower'">
      <path d="M50 83V43m0 32c20 0 25-9 25-17-13 1-22 7-25 17" stroke="#577B4C" stroke-width="3" fill="#91AA70"/>
      <g fill="#D9AA4F"><ellipse cx="50" cy="24" rx="8" ry="15"/><ellipse cx="50" cy="60" rx="8" ry="15"/><ellipse cx="32" cy="42" rx="15" ry="8"/><ellipse cx="68" cy="42" rx="15" ry="8"/><ellipse cx="37" cy="29" rx="8" ry="15" transform="rotate(-45 37 29)"/><ellipse cx="63" cy="29" rx="8" ry="15" transform="rotate(45 63 29)"/><ellipse cx="37" cy="55" rx="8" ry="15" transform="rotate(45 37 55)"/><ellipse cx="63" cy="55" rx="8" ry="15" transform="rotate(-45 63 55)"/></g>
      <circle cx="50" cy="42" r="15" fill="#806143"/><g fill="#B08B52"><circle cx="45" cy="38" r="2"/><circle cx="54" cy="40" r="2"/><circle cx="49" cy="47" r="2"/></g>
    </g>
    <g v-else-if="name === 'acorn'" stroke="#846449" stroke-width="3" stroke-linejoin="round">
      <path d="M28 43c0 28 6 36 23 43 17-7 23-18 23-43" fill="#CDA36E"/><path d="M22 45c1-31 57-31 58 0-19 8-40 8-58 0Z" fill="#9F835C"/><path d="M50 23c0-9 6-14 12-15" fill="none" stroke-linecap="round"/><path d="m33 34 6 8m9-11 6 12m9-9 4 8" stroke="#C3AA7B"/>
    </g>
    <g v-else-if="name === 'lavender'" stroke="#638050" stroke-width="2.5" stroke-linecap="round">
      <path d="M49 87V24M49 73 31 38m18 30 19-32"/><g fill="#A798BB" stroke="#8B7B9F" stroke-width="1.5"><ellipse cx="48" cy="22" rx="6" ry="9"/><ellipse cx="43" cy="35" rx="6" ry="9" transform="rotate(-30 43 35)"/><ellipse cx="54" cy="40" rx="6" ry="9" transform="rotate(25 54 40)"/><ellipse cx="30" cy="34" rx="6" ry="9" transform="rotate(-25 30 34)"/><ellipse cx="35" cy="49" rx="6" ry="9" transform="rotate(-30 35 49)"/><ellipse cx="70" cy="32" rx="6" ry="9" transform="rotate(25 70 32)"/><ellipse cx="64" cy="47" rx="6" ry="9" transform="rotate(25 64 47)"/></g>
    </g>
    <g v-else-if="name === 'mark'" fill="currentColor">
      <ellipse cx="50" cy="29" rx="12" ry="21"/><ellipse cx="50" cy="71" rx="12" ry="21"/><ellipse cx="29" cy="50" rx="21" ry="12"/><ellipse cx="71" cy="50" rx="21" ry="12"/><circle cx="50" cy="50" r="15" fill="#D7B36A"/>
    </g>
  </svg>
</template>
