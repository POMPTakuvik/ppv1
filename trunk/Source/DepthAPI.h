// 
//  DepthAPI.h
//  
//  Created by Maxime Benoit-Gagne on 2017-01-05.
//  Takuvik - Canada.
//  
//  compiler:
//  $ g++ -v
//  Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1
//  Apple LLVM version 5.1 (clang-503.0.40) (based on LLVM 3.4svn)
//  Target: x86_64-apple-darwin12.6.0
//  Thread model: posix
//  
//  usage:
//  ./test_DepthAPI.c
//  
//  description:
//   Depth C-language API.
//  
//  uses: 
//  
//  keywords: C, API, depth

#ifndef __DepthAPI__h
#define __DepthAPI__h

#include "Color.h"
#include "Depth_params.h"

#ifdef __cplusplus
#   define API extern "C"
#else
#   define API
#endif

/* ====================== Prototypes ====================== */
API void* Depth_create(float array2d_idepthphy_itime_PAR[NBDEPTHS][NTIMES],
		       int idepthphy_max,
		       float depthphy_step);
API int Depth_get_array1d_itime_idepthphy_max(void* depth,
					      int array1d_itime_idepthphy_max
					      [NTIMES]);
API int Depth_to_string(void* depth,
			char* s_arg,
			int buffersize);
API void Depth_delete(void* depth);

#endif /* define(__DepthAPI__h) */
