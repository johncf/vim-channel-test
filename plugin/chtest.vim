function TestStart()
  let server = expand('<sfile>:p:h') . '/test.py'
  let err_log = expand('<sfile>:p:h') . '/chtest.err'
  let cmd = ['python3', server]
  return job_start(cmd, { 'in_mode': 'json',
                        \ 'out_mode': 'json',
                        \ 'out_cb': 'MyHandler',
                        \ 'err_mode': 'raw',
                        \ 'err_io': 'file',
                        \ 'err_name': err_log})
endfun

func MyHandler(ch, msg)
  echo "server says: " . a:msg
endfunc

let g:my_job = TestStart()
let g:my_ch = job_getchannel(g:my_job)
