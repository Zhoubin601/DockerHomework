export async function api(path, options = {}) {
  let response
  try {
    response = await fetch(`/api${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...options.headers },
      signal: AbortSignal.timeout(12000),
    })
  } catch {
    throw new Error('暂时连接不到花园，请检查服务是否启动，再重试。')
  }
  if (response.status === 204) return null
  let data
  try { data = await response.json() } catch { throw new Error('服务返回了异常响应，请稍后重试。') }
  if (!response.ok) {
    const error = new Error(data.message || '操作没有完成，请再试一次。')
    error.status = response.status
    throw error
  }
  return data
}

export const post = (path, data) => api(path, { method: 'POST', body: JSON.stringify(data) })
