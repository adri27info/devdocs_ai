<template>
  <footer
    class="w-full bg-white text-black flex flex-col sm:flex-row justify-around items-center h-24 border-t-2"
  >
    <div>
      <p>&copy; DevDocs AI • 2025</p>
    </div>
    <div class="flex flex-row gap-4">
      <RouterLink :to="{ name: 'home' }" class="underline">Terms</RouterLink>
      <RouterLink :to="{ name: 'home' }" class="underline">Privacy</RouterLink>
      <RouterLink :to="{ name: 'home' }" class="underline">Contact</RouterLink>
    </div>
  </footer>
</template>

<script setup></script>
<style scoped></style>
