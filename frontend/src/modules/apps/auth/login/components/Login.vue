<template>
  <div class="w-full flex flex-col justify-center items-center text-center gap-5">
    <div class="w-full mt-10">
      <h1 class="text-3xl font-bold mb-5">Welcome back</h1>
      <p class="text-lg">Enter your credentials to access your account</p>
    </div>

    <form
      method="post"
      @submit.prevent="handleLogin"
      class="w-full sm:w-[480px] flex flex-col justify-center items-center gap-7 rounded sm:border-1 p-2 mb-10"
    >
      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="email">Email</label>
          <span class="text-error">*</span>
        </div>
        <input
          class="w-full p-2 border-1 rounded text-center"
          type="text"
          name="email"
          id="email"
          placeholder="Enter your email"
          v-model="loginFactory.email"
        />
        <p v-if="loginFactory.emailError" class="w-full text-error font-bold">
          {{ loginFactory.emailError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-1">
          <label class="font-bold" for="password">Password</label>
          <span class="text-error mt-1">*</span>
        </div>
        <div class="flex items-center border rounded w-full p-2 relative">
          <input
            class="flex-1 text-center outline-none"
            placeholder="Enter your password"
            v-model="loginFactory.password"
            :type="passwordProps.type"
          />
          <button type="button" class="absolute right-2" @click="togglePasswordVisibility">
            <component :is="passwordProps.icon" class="h-5 w-5" />
          </button>
        </div>
        <p v-if="loginFactory.passwordError" class="w-full text-error font-bold">
          {{ loginFactory.passwordError }}
        </p>
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-2">
        <div class="w-full flex flex-row justify-center items-center gap-2">
          <input
            type="checkbox"
            name="remember"
            id="remember"
            class="mt-1"
            v-model="loginFactory.rememberMe"
          />
          <label for="remember">Remember me</label>
        </div>
        <RouterLink :to="{ name: 'reset-password' }" class="font-bold">
          Forgot your password?
        </RouterLink>
        <Loader :loading="storeCore.loaders.login" />
      </div>

      <div class="w-full flex flex-col justify-center items-center gap-4">
        <button
          type="submit"
          class="!w-[280px] btn btn-dark"
          :class="{ disabled: storeCore.btnDisablers.loginBtn }"
        >
          Sign in
        </button>
        <RouterLink :to="{ name: 'register' }" class="font-bold">
          Don't have an account? Sign up
        </RouterLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import { useLogin } from '@/modules/apps/auth/login/composables/useLogin';
import { coreStore } from '@/modules/shared/common/stores/core/coreStore';
import Loader from '@/modules/shared/common/components/ui/Loader.vue';

const storeCore = coreStore();

const { loginFactory, passwordProps, togglePasswordVisibility, handleLogin } = useLogin();
</script>

<style scoped></style>
